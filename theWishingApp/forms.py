from django import forms
from theWishingApp.models import *

class WishForm(forms.ModelForm):
    #validaciones:

    def clean_item(self):
        item = self.cleaned_data['item']
        if len(item) < 3:
            self.add_error('item', 'Item debe tener al menos tres caracteres')
        return item

    #Campos añadidos al formulario

    #meta, fields, label, widget

    class Meta:
        model = Wish
        
        fields = ['item', 'desc']
        
        labels = {
            'item' : 'Item: ',
            'desc' : 'Descripción: ',
        }
        widgets = {
            'item' : forms.TextInput(attrs={'class': 'form-control'}),
            'desc' : forms.TextInput(attrs={'class': 'form-control'}),
        }
