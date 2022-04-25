from django.contrib import admin

from core.admin import ModelAdmin, TabularInline
from .models import *


# Inlines
class ComponentInline(TabularInline):
    model = MadeReagent.item.through
    fieldsets = [
        [None, {"fields": ["item"], "classes": []}],
    ]


class StorageInline(TabularInline):
    extra = 1
    model = Storage


class CriteriaInline(TabularInline):
    extra = 1
    model = Criteria


# ModelAdmins
@admin.register(Manufacturer)
class ManufacturerAdmin(ModelAdmin):
    list_display = ["name", "model_actions"]
    list_display_links = ["name",]
    search_fields = ["name"]


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    inlines = [CriteriaInline, StorageInline]
    list_display = ["name", "type", "manufacturer", "quantity", "model_actions"]
    list_display_links = search_fields = ["name",]
    list_filter = ["type"]

    readonly_fields = ["quantity"]
    add_fieldsets = [
        [None, {"fields": ["type", "name", "manufacturer", "cost"], "classes": []}]
    ]
    fieldsets = [
        [None, {"fields": ["type", "name", "manufacturer", "cost"], "classes": []}],
        ["Other Information", {"fields": ["status", "quantity", "comment"], "classes": []}]
    ]


@admin.register(MadeReagent)
class MadeReagentAdmin(ModelAdmin):
    inlines = [ComponentInline]
    fieldsets = [
        [None, {"fields": ["comment"], "classes": []}],
    ]
    filter_horizontal = ["item"]