from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display    = ('id','content_type','content_object','user_from','user_target','code', 'date_create', 'date_modify')
    list_filter     = ('content_type', 'user_from','user_target', 'code', 'date_create')
    raw_id_fields   = ('user_from', 'user_target')
    model           = Item

admin.site.register(Item,ItemAdmin)
