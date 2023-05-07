from django.urls import path
from django.contrib import admin
from .views import ItemView,getPagination,getNumberOfSuppliers,getNumberOfLocations,getNumberOfMachines,getcalculatetotalprices,getNumberOfItems,getItemsByRoomDesc, ItemsView, CategoriesView, CategoryView , LocationsView , LocationView , UsersView,getMissItems , UserView , UpdateItemQuantity , SuppliersView , SupplierView , HistoryView , HistoriesView , MachinesViews , MachineView , getItemByPnManufacturer,getItemBySerialNumber,getItemsByMachineId , getItemsByCategoryId , getItemsByLocationId



urlpatterns = [ 
    path('items', ItemsView),
    path('items/<str:id>', ItemView), 
    path('categories', CategoriesView),
    path('categories/<str:id>', CategoryView),
    path('locations', LocationsView),
    path('locations/<str:id>', LocationView),
    
    path('users', UsersView),
    path('users/<str:id>', UserView), 
    
    path('Suppliers', SuppliersView),
    path('Supplier/<str:id>', SupplierView), 
    path('histories', HistoriesView),
    path('history/<str:id>', HistoryView), 
    path('updateItemQuantity/<str:id>', UpdateItemQuantity),
    path('machines', MachinesViews),
    path('machine/<str:id>', MachineView),
    
    
    ## All Gets from server filtered
    path('getitembyman/<str:id>' , getItemByPnManufacturer) ,   # get item by P.N Manufacturer
    path('getitembyserialnumber/<str:id>' , getItemBySerialNumber) ,    # get all items with the serial number
    path('getitembymachineid/<str:id>' , getItemsByMachineId),  # get all Items with the name of spacipic machine 
    path('getitembycategoryid/<str:id>' , getItemsByCategoryId) , # get all items  with spacipic  category 
    path('getitembylocationid/<str:id>' , getItemsByLocationId) , # get all items  with spacipic  location 
    path('getmissitems/' , getMissItems) , # get all miss items is stock
    path('getitembyroomdesc/<str:id>' , getItemsByRoomDesc) , # get all miss items is stock
    
    ## All Data 
    path('getnumberofitems' ,getNumberOfItems )  , # Calc Number of Items
    path('getnumberofsuppliers' ,getNumberOfSuppliers )  , # Calc Number of Items
    path('getnumberoflocations' ,getNumberOfLocations )  , # Calc Number of Items
    path('getnumberofmachines' ,getNumberOfMachines )  , # Calc Number of Items
    path('getallitemprice' ,getcalculatetotalprices ) ,  # get item by P.N Manufacturer
    
    # Pages
    path('getpages/<str:page>/', getPagination),
    # path('getphilipsnumber/>/', getPhilipsNumber),
    
    
]
