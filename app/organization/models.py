from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from common.utils.images import resize_image


class Organization(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='images/organization/default.png', upload_to='images/organization')
    slug = models.SlugField(unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_organizations')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owning_organizations')
    administrators = models.ManyToManyField(User, related_name='administrating_organizations', blank=True)
    members = models.ManyToManyField(User, blank=True, related_name='organizations')
    type = models.ForeignKey('game.GameType', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('organization-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        resize_image(self.image.path, 300, 300)
