from django.contrib import admin
from .models import Profile, Project, ContactMessage

# Admin panel ko thoda professional look dene ke liye
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent')
    readonly_fields = ('name', 'email', 'subject', 'message', 'date_sent') # Taaki message koi edit na kar sake

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(ContactMessage, ContactMessageAdmin)