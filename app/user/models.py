from django.db import models
from django.contrib.auth.models import User
from common.utils.images import resize_image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='images/user/profile/default.png', upload_to='images/user/profile')

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super().save(args, kwargs)
        resize_image(self.image.path, 300, 300)


class Group(models.Model):
    name = models.CharField(max_length=100)
    administrators = models.ManyToManyField(User, related_name='administrating_groups')
    users = models.ManyToManyField(User)
    image = models.ImageField(default='images/user/group/default.png', upload_to='images/user/group')

    def __str__(self):
        return f'{self.name} group'
