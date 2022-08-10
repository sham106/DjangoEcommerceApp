from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from models import *
# User = get_user_model()
User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()
