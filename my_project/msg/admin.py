from django.contrib import admin
from .models import *

class MsgAdmin(admin.ModelAdmin):
    list_display=['assunto', 'grupo', 'importancia', 'create_at']
    search_fields = ['assunto', 'grupo']

admin.site.register(Group_Msg)
admin.site.register(Msg, MsgAdmin)

# Register your models here.
