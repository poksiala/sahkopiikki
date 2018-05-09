from django.contrib import admin
from api.models import *

admin.site.disable_action('delete_selected')
admin.site.register(Product)

def set_done(modeladmin, request, queryset):
    queryset.update(done=True)

set_done.short_description = "Mark selected transactions as done"

def set_not_done(modeladmin, request, queryset):
    queryset.update(done=False)

set_not_done.short_description = "Mark selected transactions as not done"

class TransactionAdmin(admin.ModelAdmin):
  list_display = ('name', 'user', 'price_in_euros', 'timestamp', 'done')
  actions = [set_done, set_not_done]

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'balance')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
