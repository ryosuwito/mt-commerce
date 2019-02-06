from django import forms
from database_wilayah.models import Provinsi

class ShippingOriginForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    provinsi = forms.ModelChoiceField(Provinsi.objects.all(), initial='')
    kota = forms.CharField(max_length=200, required=True)
    kecamatan = forms.CharField(max_length=200, required=True)
    kelurahan = forms.CharField(max_length=200, required=True)
    alamat = forms.CharField(max_length=200, required=True)

    def __init__(self, *args, **kwargs):
        super(ShippingOriginForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['style'] = 'width:100%' 
        self.fields['provinsi'].widget.attrs['onClick'] = 'getKota(this.id)'
        self.fields['provinsi'].widget.attrs['style'] = 'width:100%' 
        self.fields['alamat'].widget = forms.Textarea() 
        self.fields['alamat'].widget.attrs['style'] = 'width:100%' 
        self.fields['alamat'].widget.attrs['rows'] = '3' 
        self.fields['alamat'].widget.attrs['placeholder'] = 'Contoh: Jl. Angkasa 1 Blok AF6 NO 18'