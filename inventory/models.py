from django.db import models
from django.core.validators import MinValueValidator

#contains suppliers
class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Manufacturer Name", max_length=150)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains items
class Item(models.Model):
    """ Stores a single item entry, related to :model:`inventory.Manufacturer`. """
    type = models.CharField("Item Type", max_length=1, choices=[("k", "kit"), ("r", "reagent"), ("c", "consumable"),], default="k", help_text="Item types: kit, reagent, consumable")
    name = models.CharField("Item Name", max_length=30)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="item_manufacturer", null=True)
    cost = models.DecimalField("Unit Cost", validators=[MinValueValidator(0.00)], default=0.00, max_digits=8, decimal_places=2)

    status = models.CharField("Item Status", max_length=1, choices=[("n", "new"), ("d", "discontinued"), ("a", "active"),], default="n", help_text="Current Status: new, discontinued, active")
    quantity = models.IntegerField(default=0, help_text="Current Item in Inventory")
    comment = models.TextField("Comments", blank=True)
    manual = models.FileField("User Manual", blank=True, null=True)

    def __str__(self):
        return self.name


class Storage(models.Model):
    """ Storage Condition and Location for :model:`inventory.Item`. """
    condition = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)


class Criteria(models.Model):
    """ Acceptable Criteria for :model:`inventory.Item`. """
    ship_temp = models.FloatField("Shipping Temperature")
    packing = models.CharField(max_length=50, blank=True, null=True)
    appearance = models.CharField(max_length=50, blank=True, null=True)
    service_life = models.CharField("Service Life", max_length=50, blank=True, null=True)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)


#contains the made reagents
class MadeReagent(models.Model):
    """ In-house Reagent compose of :model:`transactions.PurchaseItem`. """
    billno = models.AutoField(primary_key=True)
    name = models.CharField("Item Name", max_length=30)
    
    item = models.ManyToManyField("transactions.PurchaseItem", through="transactions.Component")
    comment = models.TextField("Comments", blank=True)

    class Meta:
        pass #model_name = "In-House Reagent"

    def __str__(self):
        return "Bill no: " + str(self.billno)
        
