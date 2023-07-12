import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, PermissionsMixin)
from Users.fields import IntegerRangeField
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
        _("First name"), max_length=150, blank=False, null=True)
    last_name = models.CharField(
        _("Last name"), max_length=150, blank=False, null=True)
    user_name = models.CharField(
        _("User name"), max_length=50, blank=False, null=True)
    bio = models.CharField(_("Bio"), max_length=255, blank=False, null=True)
    sex = models.CharField(
        _("Sex"), max_length=50, choices=SEX.choices, default=None, blank=True, null=True)
    profile_avatar = models.ImageField(
        _("Profile photo"), upload_to='user/Users/profile_pic', max_length=None, blank=False, null=True)
    birth_date = models.DateField(
        _("Birth day"), auto_now=False, auto_now_add=False, null=True)
    phone_number = models.CharField(
        _("phone number"), max_length=13, blank=True, null=True)
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


class Invitation(models.Model):
    '''
    A users invitation code fields: user, invitation_code, count
    '''
    user = models.ForeignKey("User", verbose_name=_(
        "User"), on_delete=models.CASCADE)
    invitation_code = models.CharField(
        _("Invitation code"), max_length=10, blank=True, null=True)
    count = models.PositiveIntegerField(
        _("Invited users count"), blank=True, null=False)
    disabled = models.BooleanField(_("Disabled"), default=False)

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
