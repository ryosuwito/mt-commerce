from django import forms
from shopping_cart.models import Cart, CartItem
from catalog.models import Category, Product
from database_wilayah.models import Provinsi

class ProductCartForm(forms.Form):
    quantity = forms.IntegerField(required=True, initial=1)

    def __init__(self, *args, **kwargs):
        super(ProductCartForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['oninput'] = 'quantityChange()'
        self.fields['quantity'].widget.attrs['style'] = 'width:100%'
        self.fields['quantity'].widget.attrs['class'] = 'input-text'

class CreateNewStoreForm(forms.Form):
    name = forms.CharField(label='Nama Toko', required=True)
    description = forms.CharField(label='Deskripsi', required=False)
    photo = forms.ImageField(label='Foto/Logo Toko', required=False)

    def __init__(self, *args, **kwargs):
        super(CreateNewStoreForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['style'] = 'width:100%'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['style'] = 'width:100%'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['style'] = 'width:100%'
        self.fields['photo'].widget.attrs['class'] = 'form-control'

class AddProductForm(forms.Form):
    EXCLUDE = ['Provinsi']
    CATEGORY_OPTIONS = Category.objects.filter(is_archived=False)
    condition = forms.ChoiceField(choices=Product.CONDITION_CHOICES,
        initial=Product.CONDITION_CHOICES[0],
        required=True, label='Kondisi Produk')
    name = forms.CharField(label='Nama', required=True)
    description = forms.CharField(label='Deskripsi', required=False, widget=forms.Textarea)
    price = forms.IntegerField(label='Harga', 
        help_text='*(Dalam Rupiah, tanpa titik/koma)',
        required=True)
    unit_weight = forms.IntegerField(label='Berat', 
        help_text='*(Dalam Gram, tanpa titik/koma)',
        required=True)
    categories = forms.ModelMultipleChoiceField(CATEGORY_OPTIONS,
        label='Kategori', initial='')
    brand = forms.CharField(label='Merk Produk', required=False)
    provinsi = forms.ModelChoiceField(Provinsi.objects.all(), initial='')
    photo = forms.ImageField(label='Foto Produk', required=True)
    photo_alt1 = forms.ImageField(label='Foto Produk 2', required=False)
    photo_alt2 = forms.ImageField(label='Foto Produk 3', required=False)

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['provinsi'].widget.attrs['onClick'] = 'getKota(this.id)'
        self.fields['provinsi'].widget.attrs['style'] = 'width:100%'
        self.fields['provinsi'].widget.attrs['class'] = 'form-control'
        self.fields['condition'].widget.attrs['style'] = 'width:100%'
        self.fields['condition'].widget.attrs['class'] = 'form-control'
        self.fields['categories'].widget.attrs['style'] = 'width:100%'
        self.fields['categories'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['style'] = 'width:100%'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['brand'].widget.attrs['style'] = 'width:100%'
        self.fields['brand'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['style'] = 'width:100%'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['style'] = 'width:100%'
        self.fields['photo'].widget.attrs['class'] = 'form-control'
        self.fields['photo_alt1'].widget.attrs['style'] = 'width:100%'
        self.fields['photo_alt1'].widget.attrs['class'] = 'form-control'
        self.fields['photo_alt2'].widget.attrs['style'] = 'width:100%'
        self.fields['photo_alt2'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['style'] = 'width:100%'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['unit_weight'].widget.attrs['style'] = 'width:100%'
        self.fields['unit_weight'].widget.attrs['class'] = 'form-control'