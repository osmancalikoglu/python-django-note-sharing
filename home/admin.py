from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage

admin.site.register(Setting)


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'note']
    list_filter = ['status']


admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
