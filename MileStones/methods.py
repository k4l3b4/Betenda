from .models import TYPE_CHOICES, MileStone


def give_achievements(user, milestone):
    try:
        MileStone.objects.create(user=user, milestone=milestone)
    except:
        pass