'''Schafer, C. (2019). CoreyMSchafer/code_snippets. [online]
GitHub. Available at: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
[Accessed 1 Dec. 2018].'''
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile (models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE) #cascade one way, if user deleted, delete profile. If delete profile not delete user- one way
    image= models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img= Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size= (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
