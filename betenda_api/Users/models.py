import random
import string
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, PermissionsMixin)
from Users.fields import IntegerRangeField
from django_extensions.db.fields import RandomCharField
# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned as a staff.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned as a superuser.')

        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):

        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Avatar(models.Model):
    class TYPE(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"

    media = models.FileField(
        _("Profile media"), upload_to='user/Users/profile', max_length=None, blank=True, null=True)
    type = models.CharField(
        _("Media type"), choices=TYPE.choices, max_length=255)
    posted_at = models.DateTimeField(
        _("Posted date"), auto_now=False, auto_now_add=True)


class User(AbstractBaseUser, PermissionsMixin):
    '''
    The default User model
    '''
    class SEX(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    email = models.EmailField(
        _("Email"), max_length=254, unique=True, default=None, blank=False, null=True)
    first_name = models.CharField(
        _("First name"), max_length=150, blank=False)
    last_name = models.CharField(
        _("Last name"), max_length=150, blank=False, null=True)
    user_name = models.CharField(
        _("User name"), max_length=50, blank=False)
    bio = models.CharField(_("Bio"), max_length=255, blank=False, null=True)
    sex = models.CharField(
        _("Sex"), max_length=50, choices=SEX.choices, default=None, blank=True, null=True)
    profile_avatar = models.ImageField(
        _("Profile photo"), upload_to='user/profile', max_length=None, blank=True, null=True)
    birth_date = models.DateField(
        _("Birth day"), auto_now=False, auto_now_add=False, blank=True, null=True)
    invited_by = models.ForeignKey('self', verbose_name=_(
        "Invited by"), on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(
        _("phone number"), max_length=13, blank=True, null=True)
    verified = models.BooleanField(default=False)
    has_rated = models.BooleanField(_("Has rated the app"), default=False)
    terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    joined_date = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True)
    last_login = models.DateTimeField(
        _("last login"), auto_now=True, auto_now_add=False)
    deleted = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='groups'
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'user_name', 'last_name']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def save(self, *args, **kwargs):
        is_new_instance = not self.pk
        super().save(*args, **kwargs)
        if is_new_instance:
            Invitation.objects.create(user=self)


class UserProfile(models.Model):
    '''
    Model to handle Follower, Following and Friends
    '''
    user = models.OneToOneField(
        "User", verbose_name=_("User"), on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        "User", through='FollowerRequest', related_name="followers", verbose_name=_("User"))
    following = models.ManyToManyField(
        "User", related_name="following", verbose_name=_("User"))
    # needed to get the count instead of counting followers and following on each request
    followers_count = models.PositiveIntegerField(
        _("Followers count"), default=0)
    following_count = models.PositiveIntegerField(
        _("Following count"), default=0)
    is_private = models.BooleanField(_("Private account"), default=False)

    def __str__(self):
        return f"{self.user.user_name} Followers: {self.followers_count}, Following: {self.following_count}"

    class Meta:
        verbose_name = _("Friends")
        verbose_name_plural = _("Friends")

    def is_followed_by(self, user):
        """
        Check if the given user is being followed by the requesting user.
        """
        return self.followers.filter(id=user.id).exists()

    def is_following(self, user):
        """
        Check if the requesting user is following the given user.
        """
        return self.following.filter(id=user.id).exists()


class FollowerRequest(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name=_("User profile"), db_index=True)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Follower"), db_index=True)
    is_approved = models.BooleanField(_("Approved"), default=False)
    requested_at = models.DateTimeField(_("Requested at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Follower Request")
        verbose_name_plural = _("Follower Requests")


class Invitation(models.Model):
    '''
    A users invitation code fields: user, invitation_code, count
    '''
    user = models.ForeignKey("User", verbose_name=_(
        "User"), on_delete=models.CASCADE, db_index=True)
    invitation_code = RandomCharField(
        _("Invitation code"), length=15, unique=True, blank=True, null=True)
    count = models.IntegerField(
        _("Invited users count"), default=0, blank=True, null=True)
    disabled = models.BooleanField(_("Disabled"), default=False)
    expired = models.BooleanField(_("Expired"), default=False)

    class Meta:
        verbose_name = _("Invitation code")
        verbose_name_plural = _("Invitation codes")


class Password_reset(models.Model):
    """
    Password reset management table, takes email, otp, created_at and updated_at
    """
    email = models.EmailField(
        _("Email"), max_length=254, unique=True, default=None, blank=True, null=True)
    otp = IntegerRangeField(
        min_value=100000, max_value=999999, blank=True, null=True)
    created_at = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True, blank=False)
    expires_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.email

    @property
    def expired(self):
        """
        returns a boolean value based on weather the time has passed timezone.now()
        """
        return self.expires_at < timezone.now()

    class Meta:
        verbose_name = _("Password reset OTP")
        verbose_name_plural = _("Password reset OTPS")


class Device(models.Model):
    user = models.ForeignKey("User", verbose_name=_(
        "User"), on_delete=models.CASCADE, blank=False, null=True)
    ip_address = models.CharField(
        _("Ip address"), max_length=255, blank=False, null=True)
    device_type = models.CharField(
        _("Device Type"), max_length=255, blank=False, null=True)
    browser_type = models.CharField(
        _("Device Type"), max_length=255, blank=False, null=True)
    browser_version = models.CharField(
        _("Device Type"), max_length=255, blank=False, null=True)
    device_name = models.CharField(
        _("Device name"), max_length=255, blank=False, null=True)
    city = models.CharField(
        _("City name"), max_length=255, blank=False, null=True)
    country = models.CharField(
        _("Country name"), max_length=255, blank=False, null=True)
    operating_system = models.CharField(
        _("Operating system"), max_length=255, blank=False, null=True)
    logged_in = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
