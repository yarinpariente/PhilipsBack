import json
from functools import reduce
from django.db.models import F
from math import ceil
import threading
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render , redirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import Item , Category , Location , User , Supplier , History , Machine , Room 
from .serializers import ItemSerializer,ItemPostSerializer , CategorySerializer , LocationSerializer , UserSerializer , SupplierSerializer , HistorySerializer , MachineSerializer , RoomSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


def send_email_async(subject, message, from_email, recipient_list):
    """
    Helper function to send email asynchronously using threading.
    """
    threading.Thread(target=send_mail, args=(subject, message, from_email, recipient_list)).start()
    

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
                machine.counter_item_machine += 1
                machine.save()
                request.data['machine'] = machine.machine_id
                # newp_n = machine.machine_serial_number + machine.counter_item_machine
                # request.data['pn_philips'] = newp_n
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
            return JsonResponse(serializer.data,status=200,safe=False)

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
                new_machine_data = request.data.pop('machine')
                new_machine, created = Machine.objects.get_or_create(name=new_machine_data['name'])
                new_counter = new_machine.counter_item_machine + 1
                new_machine.counter_item_machine = new_counter
                new_machine.save()

                old_machine = item.machine
                if old_machine != new_machine:
                    old_counter = old_machine.counter_item_machine - 1
                    old_machine.counter_item_machine = old_counter
                    old_machine.save()
                request.data['machine'] = new_machine.machine_id
            ser = ItemPostSerializer(instance = item , data=request.data , partial = True)
            if ser.is_valid():
                item_created = ItemSerializer(ser.save())
                # Sending email to manager 
                if( item_created.data['quantity'] != item.last_quantity) :
                    item.last_quantity = item_created.data['quantity']
                    item.save()
                    if item_created.data['quantity'] <= item_created.data['limit']:
                        subject = 'Item {} is under the Limit'.format(item_created.data['name'])
                        message = 'The item "{}" Have {} in stock its under the limit {} . Please order.'.format(item_created.data['name'],item_created.data['quantity'],item_created.data['limit'])
                        from_email = 'philipsmaintenance86@gmail.com'
                        recipient_list = ['yarinpariente10@gmail.com']  # Update with your recipient list
                        send_email_async(subject, message, from_email, recipient_list)
                return JsonResponse(item_created.data, safe=False, status=201)
            return JsonResponse(ser.errors, status=400 , safe=False)
        
        elif request.method == 'DELETE':
            machine = item.machine
            item.delete()
            machine.counter_item_machine -= 1
            machine.save()
            return JsonResponse(f'The resource with id {id} deleted',safe=False, status=200)

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
              return JsonResponse(ser.data, safe=False, status=200)
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
              return JsonResponse(ser.data,safe=False, status=200)
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

@api_view(['GET','POST'])
def MachinesViews(request):
    try:
        if request.method == 'GET': # list all items
            machines = Machine.objects.all()
            ser = MachineSerializer(machines, many=True)
            return JsonResponse(ser.data,safe=False, status=200)
        
        if request.method == 'POST':  # create a new item           
            machine = Machine()
            ser = MachineSerializer(machine, data=request.data)
            if ser.is_valid():
                last_machine = Machine.objects.order_by('-machine_id').first()
                if last_machine is None:
                    serial_number = 10000
                else:
                    serial_number = int(last_machine.machine_serial_number) + 1000
            # generate unique serial number
            while Machine.objects.filter(machine_serial_number=serial_number).exists():
                serial_number += 1000
            ser.validated_data['machine_serial_number'] = serial_number
            ser.save()
            return JsonResponse(ser.data, safe=False, status=201)
        return JsonResponse(ser.errors, status=400)
        
    except Exception as e:
        return JsonResponse(f'{e}', safe=False, status=500)
       
@api_view(['GET', 'PUT', 'DELETE'])
def MachineView(request, id):
    try:
        # Check if the machine with the given id exists
        try:
            machine = Machine.objects.get(pk=id)
        except Machine.DoesNotExist:
            return JsonResponse(f'The resource with id {id} does not exist', safe=False, status=404)
        
        if request.method == 'GET':
            # Get the machine with the given id
            ser = MachineSerializer(machine)
            return JsonResponse(ser.data, safe=False, status=200)
        
        elif request.method == 'PUT':
            # Update the machine with the given id
            ser = MachineSerializer(instance=machine, data=request.data, partial=True)
            if ser.is_valid():
                ser.save()
                return JsonResponse(f'The resource with id {id} updated', safe=False, status=200)
            return JsonResponse(ser.errors, status=400)
        
        elif request.method == 'DELETE':
            # Delete the machine with the given id
            machine.delete()
            return JsonResponse(f'The resource with id {id} deleted', safe=False, status=200)
        
    except Exception as e:
        # Return an error response if an exception is raised
        return JsonResponse(f'{e}', safe=False, status=500)




    
@api_view(['GET'])
def getItemByPnManufacturer(request, id):   ## return the item that have the same P/N Manufacturer
    try:
        item = Item.objects.filter(pn_manufacturer=id).first()
        if item:
            ser = ItemSerializer(item)
            return JsonResponse(ser.data, status=200)
        else:
            return JsonResponse({'error': 'Item not found.'}, status=404)
    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
@api_view(['GET'])
def getItemBySerialNumber(request, id): ## return all items that have the same Serial Number
    try:
        items = Item.objects.filter(serial_number=id)
        if items.exists():
            ser = ItemSerializer(items, many=True)
            return JsonResponse(ser.data, status=200, safe=False)
        else:
            return JsonResponse({'error': 'Items not found.'}, status=404)
    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
    
@api_view(['GET'])
def getItemsByMachineId(request, id):   ## return all items that have the same Machine
    try:
        items = Item.objects.filter(machine = id)
        if items.exists():
            ser = ItemSerializer(items, many=True)
            return JsonResponse(ser.data, status=200, safe=False)
        else:
            return JsonResponse({'error': 'Items not found.'}, status=404)
    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
@api_view(['GET'])
def getItemsByCategoryId(request, id):  ## return all items that have the same Category
    try:
        items = Item.objects.filter(category = id)
        if items.exists():
            ser = ItemSerializer(items, many=True)
            return JsonResponse(ser.data, status=200, safe=False)
        else:
            return JsonResponse({'error': 'Items not found.'}, status=404)
    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)

@api_view(['GET'])
def getItemsByLocationId(request, id):  ## return all items that have the same location
    try:
        items = Item.objects.filter(room = id)
        if items.exists():
            ser = ItemSerializer(items, many=True)
            return JsonResponse(ser.data, status=200, safe=False)
        else:
            return JsonResponse({'error': 'Items not found.'}, status=404)
    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)


@api_view(['GET'])
def getMissItems(request):  ## Get all items Misses items in stock thah quantity <= limit
    try:
        items = Item.objects.filter(quantity__lte=F('limit'))
        if items.exists():
            ser = ItemSerializer(items, many=True)
            return JsonResponse(ser.data, status=200, safe=False)
        else:
            return JsonResponse({'error': 'No low stock items found.'}, status=404)
    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
@api_view(['GET'])
def getItemsByRoomDesc(request, id):    ## Get all items with the same sescription
    try:
        items = Item.objects.filter(room_description__iexact=id.lower())
        if items.exists():
            ser = ItemSerializer(items, many=True)
            return JsonResponse(ser.data, status=200, safe=False)
        else:
            return JsonResponse({'error': 'Items not found.'}, status=404)
    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
@api_view(['GET'])
def getNumberOfItems(request):    ## Counter All Items
    try:
        count  = Item.objects.all().count()
        return JsonResponse(count, safe=False, status=200)

    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
@api_view(['GET'])
def getNumberOfSuppliers(request):    ## Counter All Suppliers
    try:
        count  = Supplier.objects.all().count()
        return JsonResponse(count, safe=False, status=200)

    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
@api_view(['GET'])
def getNumberOfLocations(request):    ## Counter All Locations
    try:
        count  = Location.objects.all().count()
        return JsonResponse(count, safe=False, status=200)

    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
@api_view(['GET'])
def getNumberOfMachines(request):    ## Counter All Locations
    try:
        count  = Machine.objects.all().count()
        return JsonResponse(count, safe=False, status=200)

    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)

@api_view(['GET']) 
def getcalculatetotalprices(request):
    try:
        all_items = Item.objects.all()
        total_price = reduce(lambda acc, item: acc + item.price * item.quantity, all_items, 0)
        return JsonResponse(total_price, safe=False, status=200)

    except Exception as e:
        print(str(e))  # print the error message to help with debugging
        return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)
    
    
## Pagessss Items
@api_view(['GET'])
def getPagination(request, page):
    items_per_page = 2 # set the number of items per page
    paginator = Paginator(Item.objects.all(), per_page=items_per_page)
    total_items = Item.objects.all().count()
    total_pages = ceil(total_items / items_per_page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    serializer = ItemSerializer(items, many=True)
    response_data = {
        "total_items":total_items,
        'total_pages': total_pages,
        'items': serializer.data
    }
    return JsonResponse(response_data,safe=False, status=200)


# @api_view(['GET']) 
# def getPhilipsNumber(request,id):
#     try:
#         # Check if the machine with the given id exists
#         try:
#             machine = Machine.objects.get(pk=id)
#         except Machine.DoesNotExist:
#             return JsonResponse(f'The resource with id {id} does not exist', safe=False, status=404)
        
#             if request.method == 'GET':
#             # Get the machine with the given id
#                 ser = MachineSerializer(machine)
#             return JsonResponse(ser.data.counter_item_machine, safe=False, status=200)

#     except Exception as e:
#         print(str(e))  # print the error message to help with debugging
#         return JsonResponse({'error': 'Internal server error.'}, safe=False, status=500)