"""Model admin configuration."""
from django.contrib import admin
from api.models import Transaction, Product, UserProfile

admin.site.disable_action('delete_selected')

def set_done(modeladmin, request, queryset):
  """Action to set model done field as True."""
  #pylint: disable=W0613
  queryset.update(done=True)

set_done.short_description = "Mark selected transactions as done"

def set_not_done(modeladmin, request, queryset):
  """Action to set model done field as False."""
  #pylint: disable=W0613
  queryset.update(done=False)

set_not_done.short_description = "Mark selected transactions as not done"

def set_profile_all_done(modeladmin, request, queryset):
  """Action to set all transactions as True."""
  #pylint: disable=W0613
  for user in queryset:
    transactions = Transaction.objects.filter(user=user).update(done=True)

set_profile_all_done.short_description = "Mark all transactions as done for profile"

class TransactionAdmin(admin.ModelAdmin):
  """Transaction admin."""
  list_display = ('name', 'user', 'price_in_euros', 'timestamp', 'done')
  actions = [set_done, set_not_done]

class UserProfileAdmin(admin.ModelAdmin):
  """User Profile admin."""
  list_display = ('user', 'balance', 'visible')
  actions = [set_profile_all_done]

class ProductAdmin(admin.ModelAdmin):
  """Product admin."""
  list_display = ('name', 'price_in_euros', 'visible')

admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
