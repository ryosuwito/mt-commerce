from django.db import models
from database_wilayah.models import Provinsi, Kota, Kecamatan, Kelurahan

class ShippingOrigin(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    provinsi = models.ForeignKey(Provinsi, null=True, on_delete=models.SET_NULL)
    kota = models.ForeignKey(Kota, null=True, on_delete=models.SET_NULL)
    kecamatan = models.ForeignKey(Kecamatan, null=True, on_delete=models.SET_NULL)
    kelurahan = models.ForeignKey(Kelurahan, null=True, on_delete=models.SET_NULL)
    alamat = models.CharField(max_length=400, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    def __str__(self):
        return self.name.title()

    def set_default(self):
        origins = ShippingOrigin.objects.all()
        for origin in origins:
            origin.is_default = False
            origin.save()
        self.is_default = True
        self.save()