from rest_framework import serializers
from collections import OrderedDict
from uuid import UUID
from django.contrib.auth.forms import UserCreationForm
import uuid
from .models import Item , Category , Location  , Supplier  , Machine , Room , MonthlyCost , History , LatestReset
from stockmgmgt.models import User



class LatestResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestReset
        fields = '__all__'

class MonthlyCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyCost
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

  
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'  
        
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    supplier = SupplierSerializer()
    room = LocationSerializer()
    machine = MachineSerializer()

    class Meta:
        model = Item
        fields = '__all__' 
               
class ItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'        
        
        
class HistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()   # Forgin key connect 
    class Meta:
        model = History
        fields = '__all__'
        
class CustomUserCreationForm(UserCreationForm):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id_number', 'username', 'name', 'lastname', 'email', 'phone', 'job', 'unit', 'worker_number', 'is_superuser']
        
