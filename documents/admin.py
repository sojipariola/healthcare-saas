from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("file", "patient", "uploaded_by", "uploaded_at", "description")
    search_fields = ("file", "patient__name", "uploaded_by__username", "description")
    list_filter = ("uploaded_at",)
