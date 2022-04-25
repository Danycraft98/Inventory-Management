from uuid import uuid4

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

from inventory.models import Item, MadeReagent

#contains suppliers
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Supplier Name', max_length=150)
    phone = models.CharField('Phone No.', max_length=12, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    gstin = models.CharField('GSTIN No.', max_length=15, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.UUIDField("Bill No.", primary_key=True, default=uuid4())
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchasesupplier')

    request_date = models.DateTimeField("Request Date", auto_now=True)
    request_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests', default=1)
    
    order_date = models.DateTimeField("Order Date", blank=True, null=True)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)

    comment = models.TextField('Comments', blank=True)
    invoice_image = models.FileField('PO Request', blank=True, null=True)

    def __str__(self):
        return "Bill no: " + str(self.billno)

    @property
    def item_count(self):
        return self.items.count()

    @property
    def is_ordered(self):
        return self.order_date is not None

    @property
    def status(self):
        if not self.is_ordered:
            msg = 'Requested Only'
        elif all('Not' in item.status for item in self.items.all()):
            msg = 'Order Placed'
        elif all('All' in item.status for item in self.items.all()):
            msg = 'All Items Received'
        else:
            msg = 'Partially Received'
        return msg


    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.totalprice
        return total
    

#contains the purchase stocks made
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='items')
    stock = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.DecimalField("Unit Cost", validators=[MinValueValidator(0.00)], default=0.00, max_digits=8, decimal_places=2)

    received = models.IntegerField("Received Quantity", default=0)
    received_date = models.DateTimeField("Received Date", blank=True, null=True)

    @property
    def totalprice(self):
        return self.quantity * self.perprice

    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

    @property
    def status(self):
        if not self.received:
            msg = 'Not Received'
        elif self.received < self.quantity:
            msg = 'Partially Received'
        else:
            msg = 'All Received'
        return msg


#contains components
class Component(models.Model):
    billno = models.ForeignKey(MadeReagent, on_delete=models.CASCADE, related_name='components', null=True)
    item = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE, related_name='components', null=True)
    comment = models.TextField('Comments', blank=True)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

    @property
    def stock(self):
        return self.item.stock
