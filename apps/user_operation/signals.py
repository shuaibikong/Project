from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.http import HttpResponse

from .models import UserOperation, UserAction, Comments


@receiver(post_delete, sender=UserAction)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    if instance.action == 1:
        article = instance.article
        article.fav_num -= 1
        article.save()


