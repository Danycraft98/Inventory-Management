import django_filters as filter
import django_tables2 as tables

from .models import Supplier, PurchaseBill

__all__ = ['SupplierFilter', 'SupplierTable', 'PurchaseBillFilter', 'PurchaseBillTable']


class SupplierFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Supplier
        fields = ['name']


class PurchaseBillFilter(filter.FilterSet):
    billno = filter.NumberFilter(lookup_expr='icontains')
    class Meta:
        model = PurchaseBill
        fields = ['billno']


class SupplierTable(tables.Table):
    name = tables.LinkColumn("supplier", args=[tables.A("name")])
    edit = tables.LinkColumn("edit-supplier", args=[tables.A("pk")], verbose_name='Edit', text="Edit Details", attrs={'a' :{'class': 'btn btn-outline-success'}})
    delete = tables.LinkColumn("edit-supplier", args=[tables.A("pk")], verbose_name='Delete', text="Delete Stock", attrs={'a' :{'class': 'btn btn-outline-danger'}})

    class Meta:
        model = Supplier
        fields = ['name', 'gstin', 'phone', 'edit', 'delete']
        template_name = "partials/_table.html"


class PurchaseBillTable(tables.Table):
    name = tables.LinkColumn("edit-stock", args=[tables.A("pk")])
    item_count = tables.Column(verbose_name='Stocks Purchased', accessor='get_items_list().count()') #Total Purchased Price
    edit = tables.LinkColumn("edit-stock", args=[tables.A("pk")], verbose_name='Edit', text="Edit Details", attrs={'a' :{'class': 'btn btn-outline-success'}})
    delete = tables.LinkColumn("edit-stock", args=[tables.A("pk")], verbose_name='Delete', text="Delete Stock", attrs={'a' :{'class': 'btn btn-outline-danger'}})

    class Meta:
        model = PurchaseBill
        fields = ['billno', 'item_count', 'phone', 'edit', 'delete']
        template_name = "partials/_table.html"
"""<th width="10%">Bill No</th>
                <th width="15%">Supplier</th>
                <th width="15%">Stocks Purchased</th>
                <th width="10%">Quantity Purchased</th>
                <th width="15%">Total Purchased Price</th>
                <th width="10%">Purchased Date</th>
                <th width="25%">Options</th>"""