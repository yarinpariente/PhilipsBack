from django.urls import path
from django.contrib import admin
from .views import ItemView, ItemsView, CategoriesView, CategoryView , LocationsView , LocationView , UsersView , UserView , UpdateItemQuantity , SuppliersView , SupplierView , HistoryView , HistoriesView , MachinesViews , MachineView

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
]
