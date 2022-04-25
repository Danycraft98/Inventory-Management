from django.contrib import admin

from core.admin import ModelAdmin, TabularInline
from inventory.models import Item
from .models import (
    Supplier, 
    PurchaseBill, 
    PurchaseItem,
    Component
)


class PurchaseItemInline(TabularInline):
    model = PurchaseItem
    readonly_fields = ['totalprice']
    add_fieldsets = [
        [None, {'fields': ['stock', 'quantity', 'perprice', 'totalprice'], 'classes': []}],
    ]
    fieldsets = [
        [None, {'fields': ['stock', 'quantity', 'perprice', 'totalprice'], 'classes': []}],
        ['Received', {'fields': ['received_date'], 'classes': []}],
    ]

    def has_add_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_add_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj and self.has_change_permission(request, obj):
            return ['stock', 'quantity', 'perprice', 'totalprice']
        return super().get_readonly_fields(request, obj)



@admin.register(PurchaseItem)
class PurchaseItemAdmin(ModelAdmin):
    list_display = ['id', 'billno', 'stock', 'quantity', 'totalprice']
    list_display_links = ['id',]
    search_fields = ['stock']
    list_filter = ['stock__type']


@admin.register(PurchaseBill)
class PurchaseBillAdmin(ModelAdmin):
    inlines = [PurchaseItemInline]
    list_display = ['billno', 'request_date', 'status']

    readonly_fields = ['request_by', 'request_date', 'ordered_by']
    add_fieldsets = [
        [None, {'fields': ['supplier', 'comment'], 'classes': []}],
    ]
    fieldsets = [
        [None, {'fields': ['supplier', 'comment'], 'classes': []}],
        ['Request Information', {'fields': ['request_by', 'request_date'], 'classes': []}],
        ['Order Information', {'fields': ['ordered_by', 'order_date'], 'classes': []}],
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj and obj.order_date:
            PurchaseBill.objects.filter(billno=obj.billno).update(ordered_by=request.user)

    def save_related(self, request, form, formset, change):
        super().save_related(request, form, formset, change)
        if form.instance:
            for item in form.instance.items.all():
                if item.received_date and not item.received:
                    PurchaseItem.objects.filter(id=item.id).update(received=True)
                    Item.objects.filter(id=item.stock.id).update(quantity=item.stock.quantity + item.quantity)
                    for _ in range(item.quantity):
                        Component.objects.create(item=item)


@admin.register(Component)
class ComponentAdmin(ModelAdmin):
    list_display = ['id', 'item']
    list_display_links = ['id',]
    #list_editable = ['quantity']
    #quantity = tables.Column(verbose_name='Current Item in Inventory')
    search_fields = ['item']
    list_filter = ['item__stock__type']

    add_fieldsets = fieldsets = [
        [None, {'fields': ['item',], 'classes': []}],
    ]


admin.site.register(Supplier)
