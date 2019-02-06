import http.client
import json
from .models import ShippingOrigin

def set_connection():
    conn = http.client.HTTPSConnection("api.rajaongkir.com")

    headers = { 'key': "250018c61d51aac9b71cdcead9d9ab04",
    }

    return {'conn':conn, 'headers': headers}

def get_courier():
    return ['jne','pos','tiki']

def get_shipping_origin_id():
    shipping_origin = ShippingOrigin.objects.filter(is_default=True)[0]
    provinsi_origin = shipping_origin.provinsi.name
    kota_origin = shipping_origin.kota.name
    return {'provinsi_origin':provinsi_origin, 'kota_origin':kota_origin}

def get_province():
    conn = set_connection()
    conn['conn'].request("GET", "/starter/province", headers=conn['headers'])
    res = conn['conn'].getresponse()
    data = res.read()
    provinsi = json.loads(data.decode("utf-8"))['rajaongkir']['results']
    return provinsi

def get_city(province_id):
    conn = set_connection()
    conn['conn'].request("GET", 
        "/starter/city?province=%s" % (province_id), 
        headers=conn['headers'])
    res = conn['conn'].getresponse()
    data = res.read()
    kota = json.loads(data.decode("utf-8"))['rajaongkir']['results']
    return kota

def get_cost(user, courier, **kwargs):
    shipping_origin = get_shipping_origin_id()
    province_id = get_province_id(shipping_origin['provinsi_origin'])
    origin_id = get_city_id(province_id, shipping_origin['kota_origin'])
    if not user.users_cart.is_set_as_dropship :
        user_province_id = get_province_id(user.member.home_provinsi)
        destination_id = get_city_id(user_province_id, user.member.home_kota)
    else:
        user_province_id = get_province_id(user.users_cart.customer.home_provinsi)
        destination_id = get_city_id(user_province_id, user.users_cart.customer.home_kota)

    if destination_id:
        weight = user.users_cart.get_total_weight()
        payload = "origin=%s&destination=%s&weight=%s&courier=%s" % (origin_id, destination_id, weight, courier)
        conn = set_connection()
        conn['headers']['content-type'] = "application/x-www-form-urlencoded"
        conn['conn'].request("POST", "/starter/cost", payload,  headers=conn['headers'])
        res = conn['conn'].getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))['rajaongkir']
        if json_data['status']['code'] == 200:
            if json_data['results'][0]['costs']:
                try:
                    costs_list = json_data['results'][0]['costs']
                    for x in costs_list:
                        x['cost'][0]['int_value'] = x['cost'][0]['value']
                        x['cost'][0]['value'] = int_to_rupiah( x['cost'][0]['value'])
                    return costs_list
                except:
                    return 0
    return 0

def get_province_id(provinsi_name):
    provinsi_list = get_province()
    for x in provinsi_list:
        if  provinsi_name in x['province']:
            provinsi_id = x['province_id']
            break
        else :
            provinsi_id = ''
    return provinsi_id

def get_city_id(province_id, city_name):
    city_list = get_city(province_id)
    if 'Kota' in city_name :
        tipe = 'Kota'
        city_name = city_name.replace('Kota ','')
    elif 'Kabupaten' in city_name:
        tipe = 'Kabupaten'
        city_name = city_name.replace('Kabupaten ','')
    else :
        tipe = ''
    for x in city_list:
        if  city_name in x['city_name']:
            if tipe:
                if tipe == x['type']:
                    city_id = x['city_id']
                    break
            else:
                city_id = x['city_id']
                break
        else :
            city_id = ''
    return city_id

def int_to_rupiah(value):
    return 'Rp. '+ '{:,}'.format(value).replace(",",".") + ',-'