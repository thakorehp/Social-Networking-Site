from django.contrib import admin
from .models import UserProfile,Post,Friend,Room,Notification
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(
    Room,
    list_display=["id", "title", "staff_only"],
    list_display_links=["id", "title"],
)
admin.site.register(Notification)