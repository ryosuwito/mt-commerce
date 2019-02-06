from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Provinsi, Kota, Kecamatan, Kelurahan

def get_kota(request, nama_provinsi):
    if request.method == "GET":
        provinsi = Provinsi.objects.get(name=nama_provinsi)
        if provinsi:
            kota_list = Kota.objects.filter(provinsi=provinsi)
            results = []
            i = 0;
            for kota in kota_list :
                i += 1
                a = {}
                a['nama'] = kota.name
                a['value'] = kota.pk
                results.append(a)
            return JsonResponse({'results':list(results)})
        else:
            response = HttpResponse("NOT FOUND", status=404)
            return response


def get_kecamatan(request, pk):
    if request.method == "GET":
        kota = Kota.objects.get(id=pk)
        if kota:
            kecamatan_list = Kecamatan.objects.filter(kota=kota)
            results = []
            i = 0;
            for kecamatan in kecamatan_list :
                i += 1
                a = {}
                a['nama'] = kecamatan.name
                a['value'] = kecamatan.pk
                results.append(a)
            return JsonResponse({'results':list(results)})
        else:
            response = HttpResponse("NOT FOUND", status=404)
            return response

def get_kelurahan(request, pk):
    if request.method == "GET":
        kecamatan = Kecamatan.objects.get(id=pk)
        if kecamatan:
            kelurahan_list = Kelurahan.objects.filter(kecamatan=kecamatan)
            results = []
            i = 0;
            for kelurahan in kelurahan_list :
                i += 1
                a = {}
                a['nama'] = kelurahan.name
                a['value'] = kelurahan.pk
                results.append(a)
            return JsonResponse({'results':list(results)})
        else:
            response = HttpResponse("NOT FOUND", status=404)
            return response