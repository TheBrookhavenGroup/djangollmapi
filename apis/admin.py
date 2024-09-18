from django.contrib import admin
from .models import ApiKey, APIRequest


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'email', 'first_name', 'last_name', 'organization']
    readonly_fields = ['key']
    search_fields = ['key', 'email', 'first_name', 'last_name', 'organization']
    ordering = ['organization', 'last_name', 'first_name', 'email']

    def save_model(self, request, obj, form, change):
        if not obj.key:
            obj.key = ApiKey.generate_key()
        return super().save_model(request, obj, form, change)

@admin.register(APIRequest)
class APIRequestAdmin(admin.ModelAdmin):
    list_display = ['key', 'dt', 'nchars', 'nwords', 'output']
    search_fields = ['key', 'dt', 'nchars', 'nwords']
    ordering = ['dt', 'nchars', 'nwords']
    readonly_fields = ['dt', 'nchars', 'nwords', 'output']