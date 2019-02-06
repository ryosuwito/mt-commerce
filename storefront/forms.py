from django import forms
from shopping_cart.models import Cart, CartItem

class ProductCartForm (forms.Form):
    quantity = forms.IntegerField(required=True, initial=1)

    def __init__(self, *args, **kwargs):
        super(ProductCartForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['oninput'] = 'quantityChange()'
        self.fields['quantity'].widget.attrs['style'] = 'width:100%'
        self.fields['quantity'].widget.attrs['class'] = 'input-text'