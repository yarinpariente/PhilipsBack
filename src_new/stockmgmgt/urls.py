from django.contrib import admin
from .views import ItemView,getDataForEveryYear,getYearsForCalcData,getHistoryRecordsByDate,TokenExpiresView,getMonthCost,decode_token,logout_view,PasswordChangeView,login_user,create_user,getPagination,getNumberOfSuppliers,getNumberOfLocations,getNumberOfMachines,getcalculatetotalprices,getNumberOfItems,getItemsByRoomDesc, ItemsView, CategoriesView, CategoryView , LocationsView , LocationView , UsersView,getMissItems , UserView , UpdateItemQuantity , SuppliersView , SupplierView , HistoryView , HistoriesView , MachinesViews , MachineView , getItemByPnManufacturer,getItemBySerialNumber,getItemsByMachineId , getItemsByCategoryId , getItemsByLocationId
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from django.urls import path, include, re_path
from django.views.generic import TemplateView


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
    path('getmonthcost',getMonthCost) ,
    path('gethistoryrecords' , getHistoryRecordsByDate),
    path('geyyars' , getYearsForCalcData),
    path('getdataforyear' , getDataForEveryYear),
    
    
    
    
    # Pages
    path('getpages/<str:page>/', getPagination),
    # path('getphilipsnumber/>/', getPhilipsNumber),
    
    
    # Login User
    path('create_user', create_user),
    path('login_user', login_user),
    path('auth/' , include('djoser.urls')),
    path('auth/' , include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

    
    
    # Tokens for login
    path('api/token/', TokenObtainPairView.as_view()),  # Generate tokens 
    path('api/token/refresh/', TokenRefreshView.as_view()), ## Generate Update token when access id expaired , return the refrash token
    path('api/token/verify/', TokenVerifyView.as_view()),   ## check if token is ok
    path('api/token/blacklist/', TokenBlacklistView.as_view()), 
    path('api/token/expires/', TokenExpiresView.as_view()),
    path('api/token/checkToken/',decode_token) ,



    
    # Change Password 
    path('changepassword/', PasswordChangeView.as_view()),
    path('logout/', logout_view) ,# When i login i get refrash token and access token 
    


    
]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
