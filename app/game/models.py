from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from common.utils.images import resize_image


class GameType(models.Model):
    """
    GameType objects can only be created in admin back office
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Game(models.Model):
    type = models.ForeignKey(GameType, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(default='images/game/default.png', upload_to='images/game')
    players = models.ManyToManyField(User, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.type.name}'

    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(args, kwargs)
        resize_image(self.image.path, 300, 300)
