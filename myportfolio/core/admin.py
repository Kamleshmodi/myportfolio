from django.contrib import admin
from .models import Profile, Project, ContactMessage

# Admin panel ko thoda professional look dene ke liye
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent')
    readonly_fields = ('name', 'email', 'subject', 'message', 'date_sent') # Taaki message koi edit na kar sake


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'sort_order', 'live_link', 'github_link')
    list_editable = ('sort_order',)
    search_fields = ('title', 'summary', 'stack', 'badge')
    ordering = ('sort_order', 'title')

admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
