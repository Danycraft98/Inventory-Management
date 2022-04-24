from django.db import models


#contains suppliers
class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Supplier Name', max_length=150)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains stocks
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Stock Name', max_length=30, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete = models.CASCADE, related_name='stockmanufacturer', null=True)
    type = models.CharField('Stock Type', max_length=1, choices=[('k', 'kit'), ('r', 'reagent'), ('c', 'consumable'),], default='k')
    status = models.CharField('Stock Type', max_length=1, choices=[('n', 'new'), ('d', 'discontinued'), ('a', 'active'),], default='n')
    quantity = models.IntegerField(default=1)
    comment = models.TextField('Comments', blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name