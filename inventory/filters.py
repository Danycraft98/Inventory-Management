import django_filters as filter
import django_tables2 as tables

from .models import Stock    

__all__ = ['StockFilter', 'StockTable']


class StockFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Stock
        fields = ['name']


class StockTable(tables.Table):
    name = tables.LinkColumn("edit-stock", args=[tables.A("pk")], verbose_name='Stock Name')
    quantity = tables.Column(verbose_name='Current Stock in Inventory')
    options = tables.LinkColumn("edit-stock", args=[tables.A("pk")], verbose_name='Edit', text="Edit Details", attrs={'a' :{'class': 'btn btn-outline-success'}})
    delete = tables.LinkColumn("edit-stock", args=[tables.A("pk")], verbose_name='Delete', text="Delete Stock", attrs={'a' :{'class': 'btn btn-outline-danger'}})

    class Meta:
        model = Stock
        fields = ['name', 'quantity', 'options', 'delete']
        template_name = "partials/_table.html"
