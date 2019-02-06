from database_wilayah.models import Provinsi, Kota, Kecamatan, Kelurahan


with open('database_wilayah/database_indonesia.csv') as file:
    print('begin')
    provinsi = False
    kota = False
    kecamatan = False
    plimit = 34
    klimit = 100
    kclimit = 20
    kllimit = 20
    prov, kot, kec, kel = 0, 0, 0, 0
    for index, line in enumerate(file):
        print(index)
        data = line.split(';')
        data.pop(0)
        if not provinsi:
            if prov > plimit:
                break
            prov += 1
            kot, kec, kel = 0, 0, 0
            provinsi, cp = Provinsi.objects.get_or_create(name=data[0])
        elif not provinsi.name == data[0]:
            if prov > plimit:
                break
            prov += 1
            kot, kec, kel = 0, 0, 0
            provinsi, cp = Provinsi.objects.get_or_create(name=data[0])

        if not kota and not kot > klimit:    
            kot += 1
            kec, kel = 0, 0
            kota, ck = Kota.objects.get_or_create(name=('%s %s'%(data[1], data[2])), provinsi=provinsi)
        elif not kota.name == '%s %s'%(data[1], data[2]) and not kot > klimit :
            kot += 1
            kec, kel = 0, 0
            kota, ck = Kota.objects.get_or_create(name=('%s %s'%(data[1], data[2])), provinsi=provinsi)
        
        if not kecamatan and not kec > kclimit:
            kec += 1
            kel = 0
            kecamatan, ckc = Kecamatan.objects.get_or_create(name=data[3], kota=kota)
        elif not kecamatan.name == data[3] and not kec > kclimit:
            kec += 1
            kel = 0
            kecamatan, ckc = Kecamatan.objects.get_or_create(name=data[3], kota=kota)
            
        if not kel > kllimit:
            kel += 1
            kelurahan= Kelurahan.objects.get_or_create(name=data[4], kecamatan=kecamatan, postal_code = data[5].strip())
        '''
        print('%s %s'%(cp, provinsi.name))
        print('%s %s'%(ck, kota.name))
        print('%s %s'%(ckc, kecamatan.name))
        print('%s %s'%(ckl, kelurahan.name))
        print(kelurahan.postal_code)
        '''
print('done')
