from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings

from voucher_system.models import Voucher

import pyqrcode
import os 

class Member(models.Model):
    GUEST = 0
    NEW_MEMBER = 1
    DROPSHIPPER = 2
    RESELLER = 3
    AGEN = 4
    DISTRIBUTOR = 5
    MASTER_SELLER = 6

    LEVEL = {
        'DROPSHIPPER' : {
            'REFERAL_BONUS':{
                'TO_DROPSHIPPER':15000,
                'TO_RESELLER':50000,
                'TO_AGEN':250000,
                'TO_DISTRIBUTOR':400000,
            },
            'UPGRADE_THRESHOLD':25000000,
            'PURCHASING_BONUS': 1000000,
            'SELLING_BONUS': 200000,
            'TARGET': 5000000,
            'THRESHOLD': 190000,
            'BENEFIT': 5,
        },
        'RESELLER': {
            'REFERAL_BONUS':{
                'TO_DROPSHIPPER':25000,
                'TO_RESELLER':125000,
                'TO_AGEN':350000,
                'TO_DISTRIBUTOR':575000,
            },
            'UPGRADE_THRESHOLD':45000000,
            'PURCHASING_BONUS': 1400000,
            'SELLING_BONUS': 350000,
            'TARGET': 8000000,
            'THRESHOLD': 1500000,
            'BENEFIT': 10,
        },
        'AGEN': {
            'REFERAL_BONUS':{
                'TO_DROPSHIPPER':35000,
                'TO_RESELLER':200000,
                'TO_AGEN':425000,
                'TO_DISTRIBUTOR':680000,
            },
            'UPGRADE_THRESHOLD':75000000,
            'PURCHASING_BONUS': 2400000,
            'SELLING_BONUS': 600000,
            'TARGET': 13000000,
            'THRESHOLD': 6800000,
            'BENEFIT': 20,
        },
        'DISTRIBUTOR': {
            'REFERAL_BONUS':{
                'TO_DROPSHIPPER':50000,
                'TO_RESELLER':300000,
                'TO_AGEN':550000,
                'TO_DISTRIBUTOR':800000,
            },
            'UPGRADE_THRESHOLD':200000000,
            'PURCHASING_BONUS': 4800000,
            'SELLING_BONUS': 1200000,
            'TARGET': 30000000,
            'THRESHOLD': 11900000,
            'BENEFIT': 30,
        },
        'MASTER_SELLER': {
            'REFERAL_BONUS':{
                'TO_DROPSHIPPER':100000,
                'TO_RESELLER':500000,
                'TO_AGEN':750000,
                'TO_DISTRIBUTOR':1250000,
            },
            'SELLING_BONUS': 0,
            'TARGET': 0,
            'THRESHOLD': 11900000,
            'BENEFIT': 30,
        }
    }

    USER_TYPE_CHOICES = (
        (GUEST, 'Guest'),
        (NEW_MEMBER, 'New Member'),
        (DROPSHIPPER, 'Dropshipper'),
        (RESELLER, 'Reseller'),
        (AGEN, 'Agen'),
        (DISTRIBUTOR, 'Distributor'),
        (MASTER_SELLER, 'Master Seller'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE) #done
    sponsor_code = models.CharField(db_index=True, max_length=12, blank=True) #done
    referal_code = models.CharField(db_index=True, max_length=12, blank=True) #done
    sponsor = models.ForeignKey(User, on_delete=models.SET_NULL, db_index=True,  related_name="sponsor", null=True)
    member_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=NEW_MEMBER) #done
    phone_regex = RegexValidator(regex=r'^\+?62?\d{9,15}$', message="Nomor Telepon Harus memiliki format +62819999999 atau 0819999999'. Maksimal 15 Digit.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validator haruslah berupa list
    ktp_address = models.CharField(max_length=250, blank=True)
    home_address = models.CharField(max_length=250, blank=True)
    ktp_number = models.CharField(max_length=30, null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    bank_name = models.CharField(max_length=50, blank=True)
    bank_book_photo = models.ImageField(upload_to = 'bank_book_photo', blank=True)
    ktp_photo = models.ImageField(upload_to = 'ktp_photo', blank=True)
    profile_photo = models.ImageField(upload_to = 'profile_photo', blank=True)

    ktp_provinsi = models.CharField(max_length=250, blank=True)
    ktp_kota = models.CharField(max_length=250, blank=True)
    ktp_kecamatan = models.CharField(max_length=250, blank=True)
    ktp_kelurahan = models.CharField(max_length=250, blank=True)

    home_provinsi = models.CharField(max_length=250, blank=True)
    home_kota = models.CharField(max_length=250, blank=True)
    home_kecamatan = models.CharField(max_length=250, blank=True)
    home_kelurahan = models.CharField(max_length=250, blank=True)

    instagram_address = models.CharField(max_length=250, blank=True)
    facebook_address = models.CharField(max_length=250, blank=True)
    twitter_address = models.CharField(max_length=250, blank=True)
    website_address = models.CharField(max_length=250, blank=True)
    whatsapp_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    qrcode = models.CharField(max_length=60, blank=True)  

    smart_motto = models.CharField(max_length=250, blank=True)
    is_archived = models.BooleanField(default=False)
    is_member_activated = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)    
    email_verification_code = models.CharField(max_length=50, blank=True, null=True) #done
    phone_verification_code = models.CharField(max_length=5, blank=True, null=True)

    total_spent = models.PositiveIntegerField(editable=False,blank=True, null=True)
    wallet = models.PositiveIntegerField(null=True, help_text="Dompet Member", default=0)
    used_voucher = models.ManyToManyField(Voucher, 
            blank=True,
            related_name="voucher_used_by_member",
            help_text="Voucher yang dipakai member")

    @models.permalink
    def get_absolute_url(self):
        return ("membership:profile", [self.user.username,])

    def get_ktp_url(self):
        return ("/media/%s"%self.ktp_photo)

    def get_profile_photo_url(self):
        return ("/media/%s"%self.profile_photo)

    def get_bank_url(self):
        return ("/media/%s"%self.bank_book_photo)

    def get_full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_referal():
        referal_code_alpha = get_random_string(5, 
            allowed_chars='0123456789')
        referal_code_beta = get_random_string(4, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        referal_code = '%s%s'%(referal_code_alpha, referal_code_beta)
        if Member.objects.filter(referal_code= referal_code).exists():
            get_referal()
        else:
            return 'KSK{}'.format(referal_code)

    def get_qrcode(content='0123456789AB', name='default'):
        qr = pyqrcode.create('http://%s.%s/store/'%(content,settings.DEFAULT_HOST ))
        filename = "media/%s_%s.png"%(content,name)
        qr.png(filename, scale=12)
        return filename


    def get_level(self):
        level = ''
        if self.member_type == self.DROPSHIPPER :
            level = self.LEVEL['DROPSHIPPER'] 
        if self.member_type == self.RESELLER :
            level = self.LEVEL['RESELLER']
        if self.member_type == self.AGEN :
            level = self.LEVEL['AGEN']
        if self.member_type == self.DISTRIBUTOR :
            level = self.LEVEL['DISTRIBUTOR']
        if self.member_type == self.MASTER_SELLER :
            level = self.LEVEL['MASTER_SELLER']
        return level

    def copy_address(self):
        self.home_provinsi = self.ktp_provinsi
        self.home_kota = self.ktp_kota
        self.home_kecamatan = self.ktp_kecamatan
        self.home_kelurahan = self.ktp_kelurahan
        self.home_address = self.ktp_address

    def get_home_address(self):
        return '%s, %s, %s, %s - %s' % (self.home_address, 
            self.home_kelurahan, 
            self.home_kecamatan,
            self.home_kota,
            self.home_provinsi)

    def get_ktp_address(self):
        return '%s, %s, %s, %s - %s' % (self.home_address, 
            self.home_kelurahan, 
            self.home_kecamatan,
            self.home_kota,
            self.home_provinsi)

    def get_total_spent(self):
        orders = self.user.users_order.all()
        total_spent = sum([order.total_payment for order in orders])
        self.total_spent = total_spent
        return  total_spent

    def generate_new_vericode(self):
        self.email_verification_code = Member.get_number(50)
        self.save()
        return self.email_verification_code

    def get_vericode():
        return {'email_code':self.email_verification_code, 'phone_code':self.phone_verification_code}

    def get_number(amount = 50, is_num_only = False):
        if not is_num_only:
            random_number = get_random_string(amount, 
                allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_')
        else:
            random_number = get_random_string(amount, 
                allowed_chars='0123456789')
        return random_number

    def __str__(self):
        return self.get_full_name()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        member = Member(user=instance)
        member.referal_code = Member.get_referal()
        member.qrcode = Member.get_qrcode(name=member.referal_code,
            content=instance.username)
        member.email_verification_code = Member.get_number(50)
        member.phone_verification_code = Member.get_number(5, True)
        member.save()
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.member.save()

class Customer (models.Model):
    name = models.CharField(max_length=250, blank=True)
    seller = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_customer')
    home_provinsi = models.CharField(max_length=250, blank=True)
    home_kota = models.CharField(max_length=250, blank=True)
    home_kecamatan = models.CharField(max_length=250, blank=True)
    home_kelurahan = models.CharField(max_length=250, blank=True)
    home_address = models.CharField(max_length=250, blank=True)

    def get_home_address(self):
        return '%s, %s, %s, %s - %s' % (self.home_address, 
            self.home_kelurahan, 
            self.home_kecamatan,
            self.home_kota,
            self.home_provinsi)