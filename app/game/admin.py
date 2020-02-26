from django.contrib import admin
from .models import GameType, Game


class GameAdmin(admin.ModelAdmin):
    readonly_fields = ['created_by', 'type', 'organization']


admin.site.register(GameType)
admin.site.register(Game, GameAdmin)
