from django.contrib import admin
from .models import Item, User, Location, Supplier, Category , History , Room , Machine

# Register your models here.

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(History)
admin.site.register(Room)
admin.site.register(Machine)

 