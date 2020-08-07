from django.contrib import admin
from .models import MyUser, Connection, Wall
from .django_admin.account_admin import UserAdmin
from .django_admin.connection_admin import ConnectionAdmin
from .django_admin.wall_settings import WallSettings

admin.site.register(MyUser, UserAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Wall, WallSettings)
