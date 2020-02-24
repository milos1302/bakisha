from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from common.utils.images import resize_image

class Organization(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey('game.GameType', on_delete=models.PROTECT)
    administrators = models.ManyToManyField(User, related_name='administrating_organizations')
    users = models.ManyToManyField(User)
    image = models.ImageField(default='images/user/organization/default.png', upload_to='images/user/organization')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f'{self.name} organization'

    def get_absolute_url(self):
        return reverse('organization-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)
        resize_image(self.image.path, 300, 300)
