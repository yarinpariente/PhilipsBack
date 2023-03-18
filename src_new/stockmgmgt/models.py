from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# import barcode
# from barcode.writer import ImageWriter
# from io import BytesIO
# from django.core.files import File
from django.forms import ValidationError

# Create your models here.
class User(AbstractUser):
    units = (
        ("Clean Room ","C.R"),
        ("Final Test ","F.T"),
    )
    name = models.CharField(max_length=50, null=False , unique=True)
    lastname = models.CharField(max_length=50, null=False)
    email=models.EmailField(unique=True, null=False)
    phone = models.CharField(unique=True , max_length=10 , null=False )
    id_number = models.CharField(primary_key=True , max_length=50, null=False)
    job = models.CharField(max_length=50, null=False)
    unit = models.CharField(max_length=50, choices = units, null=False)
    worker_number = models.CharField(unique=True, max_length=50, null=False)
    permission = models.IntegerField(default=0) #0 worker, #1 admin
    #USERNAME_FIELD='email'
    #REQUIRED_FIELDS=['username']
        
    
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
    machine_serial_number = models.CharField(unique=True, max_length=100, null=False)
    
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
    max_column = models.IntegerField(null=False)
    max_row =  models.IntegerField(null=False)
    
    def __str__(self):
        return f'Type : {self.name}, Column: {self.max_column}, Row: {self.max_row}'
    
#
class Item(models.Model):	
    name = models.CharField(max_length=50, null=False)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null = True)
    machine = models.ForeignKey(Machine,on_delete=models.SET_NULL,null = True)
    kit_number =  models.CharField(max_length=50, null=False)
    serial_number = models.CharField(primary_key=True, max_length=100, null=False) #uniqe
    description = models.TextField(max_length=150, null=False)
    quantity = models.IntegerField(default='0', null=False)
    limit = models.IntegerField(default='0', null=False)
    supplier = models.ForeignKey(Supplier,on_delete=models.SET_NULL,null=True)
    price = models.FloatField(default='0',null = False)
    creation_date = models.DateTimeField(auto_now_add=True) #  Update
    image = models.CharField(max_length=1000000, null = True)
    room = models.ForeignKey(Location,on_delete=models.SET_NULL, null=True)
    #column = models.CharField(default = 'A',null=False , max_length=1)    from A to Z 
    column = models.IntegerField(default = '0',null=False)
    row =  models.IntegerField(default = '0',null=False) 
    room_description = models.CharField(max_length=100, null=False)
    #pn_philips = models.CharField(max_length=15, null=True)
    #pn_manufacturer = models.CharField(max_length=15, null=True)
    
    #barcode = models.ImageField(upload_to='barcodes/', blank=True)

    
    # def save(self, *args, **kwargs):
    #     EAN = barcode.get_barcode_class('ean13')
    #     ean = EAN(f'{self.pn_philips}', writer=ImageWriter())
    #     buffer = BytesIO()
    #     ean.write(buffer)
    #     self.barcode.save(f'{self.name}.png', File(buffer), save=False)
    #     return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f' Name : {self.name} , Kit Number {self.kit_number}'

#   
class History(models.Model):
    action_choices = (
        ("POST","POST"),
        ("PATCH","PATCH"),
        ("PUT","PUT"),
        ("DELETE","DELETE"),
      )
    resource_choices = (
        ("Item","Item"),
        ("Supplier","Supplier"),
        ("Category","Category"),
        ("Location","Location")
    )
    resource = models.CharField(Item, null=True , max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(choices = action_choices , max_length=10, null = False)