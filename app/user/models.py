from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from common.utils.images import resize_image


class Profile(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(default='images/user/profile/default.png', upload_to='images/user/profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} profile'

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resize_image(self.image.path, 300, 300)
