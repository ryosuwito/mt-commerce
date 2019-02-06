from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from database_wilayah.models import Provinsi, Kota, Kecamatan, Kelurahan
from .shipping_check import get_province as province
from .shipping_check import get_province_id as province_id
from .shipping_check import get_city_id as city_id
from .shipping_check import get_city as city
from .shipping_check import get_cost as cost
from .forms import ShippingOriginForm
from .models import ShippingOrigin

class SetShippingOrigin(View):
    origins = ShippingOrigin.objects.all()
    form = ShippingOriginForm()    
    @method_decorator(user_passes_test(lambda u:u.is_staff,login_url='/admin/login'))
    def post(self,request,*args, **kwargs):
        self.origins = ShippingOrigin.objects.all()
        action = request.POST.get('action', 'none')
        if(action == 'DELETE'):
            origin_pk = request.POST.get('origin_pk')
            try:
                self.origin = ShippingOrigin.objects.get(pk=origin_pk)
                self.origin.delete()
            except:
                pass
            return HttpResponseRedirect('/admin/shipping_backend/shippingorigin/')
        else:
            self.form = ShippingOriginForm(request.POST)
            if self.form.is_valid():
                response = HttpResponse("NOT OK")
                data = self.form.cleaned_data
                """
                */ cek apakah semua field lengkap, jika tidak kembalikan form 
                """
                if request.POST['provinsi'] and request.POST['kota'] and \
                request.POST['kecamatan'] and request.POST['kelurahan'] and request.POST['name']:
                    name = data.get('name')
                    alamat = data.get('alamat')
                    provinsi = Provinsi.objects.get(pk=request.POST['provinsi'])
                    kota = Kota.objects.get(pk=data.get('kota'))
                    kecamatan = Kecamatan.objects.get(pk=data.get('kecamatan'))
                    kelurahan = Kelurahan.objects.get(pk=data.get('kelurahan'))

                shipping_origin = ShippingOrigin.objects.get_or_create(name = name)[0]
                shipping_origin.provinsi = provinsi
                shipping_origin.kota = kota
                shipping_origin.kecamatan = kecamatan
                shipping_origin.kelurahan = kelurahan
                shipping_origin.alamat = alamat
                shipping_origin.save()
            return HttpResponseRedirect('/admin/shipping_backend/shippingorigin/')
    @method_decorator(user_passes_test(lambda u:u.is_staff,login_url='/admin/login'))
    def get(self,request,*args, **kwargs):
        self.origins = ShippingOrigin.objects.all()
        return render(request, "shipping_backend/set_origin.html", {"form":self.form, "origins":self.origins})

class ChangeShippingOrigin(SetShippingOrigin):
    origin = ""
    @method_decorator(user_passes_test(lambda u:u.is_staff,login_url='/admin/login'))
    def get(self, request, *args, **kwargs):
        self.form = ShippingOriginForm()    
        self.origins = ShippingOrigin.objects.all()
        try:
            self.origin = ShippingOrigin.objects.get(pk = kwargs['pk'])
        except:
            pass
        self.form.fields['provinsi'].initial=[self.origin.provinsi.pk]
        self.form.fields['name'].initial=self.origin.name
        self.form.fields['alamat'].initial=self.origin.alamat
        return render(request, "shipping_backend/set_origin.html", {"form":self.form, "origins":self.origins, 'origin':self.origin})
    def post(self, request, *args, **kwargs):
        return super(ChangeShippingOrigin, self).post(request, args, kwargs)

@user_passes_test(lambda u:u.is_staff,login_url='/admin/login')
def shipping_redirect(request, pk):
    return HttpResponseRedirect(reverse_lazy('shipping:change_origin', kwargs={'pk':pk}))

@user_passes_test(lambda u:u.is_staff,login_url='/admin/login')
def set_default(request, pk):
    try:
        origin = ShippingOrigin.objects.get(pk=pk)
        origin.set_default()
    except:
        pass
    return HttpResponseRedirect(reverse('shipping:origin'))

def get_province(request):
    return HttpResponse(province())

def get_province_id(request):
    return HttpResponse(province_id('Papua Barat'))

def get_city(request):
    return HttpResponse(city())

def get_city_id(request):
    return HttpResponse(city_id('3', 'Kabupaten Tangerang'))

def get_cost(request):
    return HttpResponse(cost(request.user, 'tiki'))