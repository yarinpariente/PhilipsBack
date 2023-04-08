import json
from django.shortcuts import render , redirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import Item , Category , Location , User , Supplier , History , Machine , Room
from .serializers import ItemSerializer,ItemPostSerializer , CategorySerializer , LocationSerializer , UserSerializer , SupplierSerializer , HistorySerializer , MachineSerializer , RoomSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@api_view(['GET','POST'])
def ItemsView(request):
    try:
        if request.method == 'GET': # list all items
            items = Item.objects.all()
            ser = ItemSerializer(items, many=True)
            return JsonResponse(ser.data,safe=False, status=200)
        elif request.method == 'POST':  # create a new item
            if 'category' in request.data:
                category_data = request.data.pop('category')
                category, created = Category.objects.get_or_create(name=category_data['name'])
                request.data['category'] = category.category_id

            if 'supplier' in request.data:
                supplier_data = request.data.pop('supplier')
                supplier, created = Supplier.objects.get_or_create(name=supplier_data['name'])
                request.data['supplier'] = supplier.supplier_id
            if 'room' in request.data:
                location_data = request.data.pop('room')
                location, created = Location.objects.get_or_create(name=location_data['name'])
                request.data['room'] = location.location_id
            if 'machine' in request.data:
                machine_data = request.data.pop('machine')
                machine, created = Machine.objects.get_or_create(name=machine_data['name'])
                request.data['machine'] = machine.machine_id
            ser = ItemPostSerializer(data=request.data)
            if ser.is_valid():
                item_created = ItemSerializer(ser.save())
                return JsonResponse(item_created.data, safe=False, status=201)
            return JsonResponse(ser.errors, status=400 , safe=False)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)

    
@api_view(['GET', 'PUT', 'DELETE'])
def ItemView(request, id):
    try:
        try:
            item = Item.objects.get(pk=id)
        except Item.DoesNotExist:
            return JsonResponse(f'The resource with id {id} does not exist', status=404)

        if request.method == 'GET':
            serializer = ItemSerializer(item)
            return JsonResponse(serializer.data, status=200)

        elif request.method == 'PUT':
            if 'category' in request.data:
                category_data = request.data.pop('category')
                category, created = Category.objects.get_or_create(name=category_data['name'])
                request.data['category'] = category.category_id

            if 'supplier' in request.data:
                supplier_data = request.data.pop('supplier')
                supplier, created = Supplier.objects.get_or_create(name=supplier_data['name'])
                request.data['supplier'] = supplier.supplier_id
            if 'room' in request.data:
                location_data = request.data.pop('room')
                location, created = Location.objects.get_or_create(name=location_data['name'])
                request.data['room'] = location.location_id
            if 'machine' in request.data:
                machine_data = request.data.pop('machine')
                machine, created = Machine.objects.get_or_create(name=machine_data['name'])
                request.data['machine'] = machine.machine_id
            ser = ItemPostSerializer(instance = item , data=request.data , partial = True)
            if ser.is_valid():
                item_created = ItemSerializer(ser.save())
                return JsonResponse(item_created.data, safe=False, status=201)
            return JsonResponse(ser.errors, status=400 , safe=False)

        elif request.method == 'DELETE':
            item.delete()
        return JsonResponse(f'The resource with id {id} deleted', status=200)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)
    

# Categoy View
@api_view(['GET','POST'])
def CategoriesView(request):
    try:
      if request.method == 'GET': # list all items
         category = Category.objects.all()
         ser = CategorySerializer(category, many=True)
         return JsonResponse(ser.data,safe=False, status=200)
      elif request.method == 'POST':  # create a new item
          ser = CategorySerializer(data=request.data) 
          if ser.is_valid():
              ser.save()
              return JsonResponse(ser.data, safe=False, status=201)
          return JsonResponse(ser.errors, status=400)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500) 
    
@api_view(['GET','PUT', 'DELETE'])
def CategoryView(request, id):
    try:
       try:
           category = Category.objects.get(pk=id)
       except Category.DoesNotExist: 
          return JsonResponse(f'the resource with id {id} does not exist', safe=False, status=404)
       if request.method == 'GET': # get a specific item
         ser = CategorySerializer(category)
         return JsonResponse(ser.data,safe=False, status=200)
       elif request.method == 'PUT':
          ser = CategorySerializer(instance = category , data=request.data , partial = True)
          if ser.is_valid():
              ser.save()
              return JsonResponse(f'the resource with id {id} updated', safe=False, status=200)
          return JsonResponse(ser.errors, status=400)
       elif request.method == 'DELETE':
           category.delete()
           return JsonResponse(f'the resource with id {id} deleted',safe=False, status=200) 
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)

# Location View 
@api_view(['GET','POST'])
def LocationsView(request):
    try:
      if request.method == 'GET': # list all items
         location = Location.objects.all()
         ser = LocationSerializer(location, many=True)
         return JsonResponse(ser.data,safe=False, status=200)
      elif request.method == 'POST':
            ser = LocationSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return JsonResponse(ser.data,safe=False, status=201)
            else:
                return JsonResponse(ser.errors, status=400)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500) 

@api_view(['GET','PUT', 'DELETE'])
def LocationView(request, id):        
    try:
       try:
           location = Location.objects.get(pk=id)
       except Location.DoesNotExist: 
          return JsonResponse(f'the resource with id {id} does not exist', safe=False, status=404)
       if request.method == 'GET': # get a specific item
         ser = LocationSerializer(location)
         return JsonResponse(ser.data,safe=False, status=200)
       elif request.method == 'PUT':
          ser = LocationSerializer(instance = location , data=request.data , partial = True)
          if ser.is_valid():
              ser.save()
              return JsonResponse(f'the resource with id {id} updated', safe=False, status=200)
          return JsonResponse(ser.errors, status=400)
       if request.method == 'DELETE':
           location.delete()
           return JsonResponse(f'the resource with id {id} deleted',safe=False, status=200) 
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)

# User View 
@api_view(['GET','POST'])
def UsersView(request):
    try:
      if request.method == 'GET': # list all items
         users = User.objects.all()
         ser = UserSerializer(users, many=True)
         return JsonResponse(ser.data,safe=False, status=200)
      elif request.method == 'POST':  # create a new item
          ser = UserSerializer(data=request.data)
          if ser.is_valid():
              ser.save()
              return JsonResponse(ser.data, safe=False, status=201)
          return JsonResponse(ser.errors, status=400)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)
    
@api_view(['GET','PUT', 'DELETE'])
def UserView(request, id): 
    try:
       try:
           user = User.objects.get(pk=id)
       except User.DoesNotExist: 
          return JsonResponse(f'the resource with id {id} does not exist', safe=False, status=404)
       if request.method == 'GET': # get a specific item
         ser = UserSerializer(user)
         return JsonResponse(ser.data,safe=False, status=200)
       if request.method == 'PUT':
          ser = UserSerializer(instance = user , data=request.data , partial = True)
          if ser.is_valid():
              ser.save()
              return JsonResponse(f'the resource with id {id} updated', safe=False, status=200)
          return JsonResponse(ser.errors, status=400)
       if request.method == 'DELETE':
           user.delete()
           return JsonResponse(f'the resource with id {id} deleted',safe=False, status=200) 
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)

# Supplier View
@api_view(['GET','POST'])
def SuppliersView(request):
    try:
      if request.method == 'GET': # list all items
         suplier = Supplier.objects.all()
         ser = SupplierSerializer(suplier, many=True)
         return JsonResponse(ser.data,safe=False, status=200)
      if request.method == 'POST':  # create a new item for an existing supplier
            ser = SupplierSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return JsonResponse(ser.data, safe=False, status=201)
            else:
                return JsonResponse(ser.errors, status=400)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)

@api_view(['GET','PUT', 'DELETE'])
def SupplierView(request,id):
    try:
       try:
           supplier = Supplier.objects.get(pk=id)
       except Supplier.DoesNotExist: 
          return JsonResponse(f'the resource with id {id} does not exist', safe=False, status=404)
       if request.method == 'GET': # get a specific item
         ser = SupplierSerializer(supplier)
         return JsonResponse(ser.data,safe=False, status=200)
       if request.method == 'PUT':
          ser = SupplierSerializer(instance = supplier , data=request.data , partial = True)
          if ser.is_valid():
              ser.save()
              return JsonResponse(f'the resource with id {id} updated', safe=False, status=200)
          return JsonResponse(ser.errors, status=400)
       if request.method == 'DELETE':
           supplier.delete()
           return JsonResponse(f'the resource with id {id} deleted',safe=False, status=200) 
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)   

# Add Or Sub Stock Quantity 
@api_view(['PUT'])
def UpdateItemQuantity(request, id):
    try:
        item = Item.objects.get(pk = id)
        body = request.data
        match body["action"]:
            case "add":
                item.quantity+=body["number"]
            case "sub":
                item.quantity-=body["number"]  
                if item.quantity < 0:
                    return JsonResponse(f'The item quantity must be greater or equel to 0 , have {item.quantity + body["number"] } available', safe=False, status=400)
        item.save()        
        return HttpResponse(f'the resource with id {id} updated' ,status=200)
    except Item.DoesNotExist:
        return JsonResponse(f'the resource with id {id} does not exist', safe=False, status=404)
    
    
# History View
@api_view(['GET','POST'])
def HistoriesView(request):
    try:
      if request.method == 'GET': # list all items
         histories = History.objects.all()
         ser = HistorySerializer(histories, many=True)
         return JsonResponse(ser.data,safe=False, status=200)
      if request.method == 'POST':  # create a new item
          ser = HistorySerializer(data=request.data , many=True , context={'safe': False})
          if ser.is_valid():
              ser.save()
              return JsonResponse(ser.data, safe=False, status=201)
          return JsonResponse(ser.errors, status=400)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)

@api_view(['GET','PUT', 'DELETE'])
def HistoryView(request,id):
    try:
       try:
        history = History.objects.get(pk=id)
       except History.DoesNotExist: 
          return JsonResponse(f'the resource with id {id} does not exist', safe=False, status=404)
       if request.method == 'GET': # get a specific item
         ser = HistorySerializer(history)
         return JsonResponse(ser.data,safe=False, status=200)
       if request.method == 'PUT':
          ser = HistorySerializer(instance = history , data=request.data , partial = True)
          if ser.is_valid():
              ser.save()
              return JsonResponse(f'the resource with id {id} updated', safe=False, status=200)
          return JsonResponse(ser.errors, status=400)
       if request.method == 'DELETE':
           history.delete()
           return JsonResponse(f'the resource with id {id} deleted',safe=False, status=200) 
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)    

# Machine View
@api_view(['GET','POST'])
def MachinesViews(request):
    try:
      if request.method == 'GET': # list all items
         machines = Machine.objects.all()
         ser = MachineSerializer(machines, many=True)
         return JsonResponse(ser.data,safe=False, status=200)
      if request.method == 'POST':  # create a new item
          ser = MachineSerializer(data=request.data)
          if ser.is_valid():
              ser.save()
              return JsonResponse(ser.data, safe=False, status=201)
          return JsonResponse(ser.errors, status=400)
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)
       
@api_view(['GET','PUT', 'DELETE'])
def MachineView(request,id):
    try:
       try:
        machine = Machine.objects.get(pk=id)
       except Machine.DoesNotExist: 
          return JsonResponse(f'the resource with id {id} does not exist', safe=False, status=404)
       if request.method == 'GET': # get a specific item
         ser = MachineSerializer(machine)
         return JsonResponse(ser.data,safe=False, status=200)
       if request.method == 'PUT':
          ser = MachineSerializer(instance = machine , data=request.data , partial = True)
          if ser.is_valid():
              ser.save()
              return JsonResponse(f'the resource with id {id} updated', safe=False, status=200)
          return JsonResponse(ser.errors, status=400)
       if request.method == 'DELETE':
           machine.delete()
           return JsonResponse(f'the resource with id {id} deleted',safe=False, status=200) 
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)
    