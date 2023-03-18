from django import forms
from .models import Item

# class StockCreateForm(forms.ModelForm): # If we want to change stock 
#     class Meta:
#         model = Item 
#         fields = ['category','mechine','kit_number','catalog_number','description','quantity','receive_quantity','limit','created_by','location','column','row','location_description']
        
# class ReviewForm(forms.Form):
#     category = forms.CharField(label = "Catrgory Name " , max_length=50)
#     mechine = forms.CharField(max_length=50,label = "Machine Name ")
#     kit_number =  forms.CharField(max_length=50, label = "Kit number  ")
#     catalog_number = forms.CharField(max_length=50,label = "PN")