from django.db import models
import uuid
from django.db import transaction
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.core.validators import RegexValidator


# id_number , username , email , worker_number


# Create your models here.
class User(AbstractUser):
    id_number = models.CharField(primary_key=True , max_length=50, null=False)
    username = models.CharField(max_length=30, null=False , unique=True)
    password = models.CharField(max_length=30, null=False )
    name = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15 , null=False )
    job = models.CharField(max_length=30, null=False)
    unit = models.CharField(max_length=30,null=False)
    worker_number = models.CharField(unique=True, max_length=50, null=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD='username'

    def __str__(self):
        return f'Name : {self.name}'
#
class Category(models.Model):
    category_id = models.UUIDField(primary_key=True ,default = uuid.uuid4, null=False , editable=False , unique=True)
    name = models.CharField(unique = True ,max_length=20, null=False)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name}'

#
class Supplier(models.Model):
    supplier_id = models.UUIDField(primary_key=True ,default = uuid.uuid4, null=False , editable=False , unique=True)
    name = models.CharField(max_length=50, null=True , unique=True )
    contact_name = models.CharField(default = "" ,max_length=20, null=False) 
    contact_phone = models.CharField(max_length=10 , null=False )
    email = models.EmailField(unique=True ,null=False)
    address = models.CharField(default = "",max_length=50, null=False) 
    
    def __str__(self):
        return f'Name : {self.name}'
    
class Machine(models.Model):
    machine_id = models.UUIDField(primary_key=True ,default = uuid.uuid4, null=False , editable=False , unique=True)
    name = models.CharField(unique=True,max_length=50, null=False)
    manufacturer = models.CharField(max_length=50, null=False)
    machine_serial_number = models.CharField(unique=True, max_length=100, null=True , blank=True) # for example first machine start from 10000,next 11000
    counter_item_machine = models.IntegerField(default=0, null=False)
    
    
        
    def __str__(self):
        return f'Name : {self.name}, manufacturer: {self.manufacturer}, machine_serial_number: {self.machine_serial_number}'
    
    
class Room(models.Model):
    room_id = models.UUIDField(primary_key=True ,default = uuid.uuid4, null=False , editable=False , unique=True)
    name = models.CharField(unique=True,max_length=50, null=False)
    
    def __str__(self):
        return f'Name : {self.name}'

#   
class Location(models.Model):
    location_id = models.UUIDField(primary_key=True ,default = uuid.uuid4, null=False , editable=False , unique=True)
    name = models.CharField(default = "" , max_length=100, null=False , unique=True )
    max_column = models.CharField(max_length=1,null=False)
    max_row =  models.IntegerField(null=False)
    
    def __str__(self):
        return f'Type : {self.name}, Column: {self.max_column}, Row: {self.max_row}'
    
class Coin(models.Model):
    coin_id = models.UUIDField(primary_key=True ,default = uuid.uuid4, null=False , editable=False , unique=True)
    name = models.CharField(default = "" , max_length=100, null=False , unique=True )
    
    def __str__(self):
        return f'Type : {self.name}'
#


class Item(models.Model):	
    name = models.CharField(max_length=50, null=False) # name of the item 
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null = True) # which categoty item belong  
    machine = models.ForeignKey(Machine,on_delete=models.SET_NULL,null = True) # which machine item belong
    kit_number =  models.CharField(max_length=50, null=True ,blank=True) # if item blong to kit of items
    serial_number = models.CharField(max_length=100 , null=True ,blank=True) # if item part of other items
    description = models.TextField(max_length=150, null=True,blank=True) # Item Description can be null
    quantity = models.IntegerField(default=0, null=False)   # Item Quantity
    last_quantity = models.IntegerField(default=-5, null=True,blank=True)    # Last Item Quantity for sends email update
    limit = models.IntegerField(default=0, null=True)   # Item Limit to send email to the manager 
    supplier = models.ForeignKey(Supplier,on_delete=models.SET_NULL,null=True)  # which Supplier give us the item 
    price = models.FloatField(default='0',null = False) # How much the item cost 
    creation_date = models.DateTimeField(auto_now_add=True) #  When create the item
    image = models.CharField(max_length=1000000, null = True,blank=True)    # Item Photo
    room = models.ForeignKey(Location,on_delete=models.SET_NULL, null=True) # which Room item belong
    column = models.CharField(max_length=1,null=False) # which column is locate in room 
    row =  models.IntegerField(null=False) # which row is locate in room 
    room_description = models.CharField(max_length=100, null=False) #  Item Description in location with box 
    pn_philips = models.CharField(primary_key=True,unique=True,max_length=15, null=False) # P/N philips to generate philips barcode
    pn_manufacturer = models.CharField(max_length=15, null=True,blank=True) # P/N manufacturer to generate philips barcode
    
    
    def move_item(item, new_machine):
        with transaction.atomic():
            old_machine = item.machine
            if old_machine != new_machine:
                old_machine.counter_item_machine -= 1
                old_machine.save()
                new_machine.counter_item_machine += 1
                new_machine.save()
                item.machine = new_machine
                item.save()
    
    def save(self, *args, **kwargs):
        if not self.pn_philips:  # if this is a new item being added
            self.machine.counter_item_machine += 1  # increment the counter
            self.machine.save()  # save the machine object to update its counter in the database
        super(Item, self).save(*args, **kwargs)
    
    def __str__(self):
        return f' Name : {self.name} , Kit Number {self.kit_number}'

#   
class History(models.Model):

    resource = models.CharField(Item, null=True , max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, null = False)
    creation_date = models.DateTimeField(default=datetime.now)
