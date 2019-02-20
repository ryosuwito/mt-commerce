from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings

from django.urls import reverse
from voucher_system.models import Voucher

import pyqrcode
import os 

class Member(models.Model):
    BUYER = 0
    SELLER = 1

    USER_TYPE_CHOICES = (
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE) #done
    member_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=BUYER) #done
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

    def get_absolute_url(self):
        return reverse("membership:profile", kwargs={'uname':self.user.username})

    def get_ktp_url(self):
        return ("/media/%s"%self.ktp_photo)

    def get_profile_photo_url(self):
        return ("/media/%s"%self.profile_photo)

    def get_bank_url(self):
        return ("/media/%s"%self.bank_book_photo)

    def get_full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_qrcode(content='0123456789AB', name='default'):
        qr = pyqrcode.create('http://%s.%s/store/'%(content,settings.DEFAULT_HOST ))
        filename = "media/%s_%s.png"%(content,name)
        qr.png(filename, scale=12)
        return filename


    def get_member_type(self):
        type = ''
        if self.member_type != self.BUYER :
            level = 'SELLER' 
        else :
            level = 'BUYER'
        return level

    def get_home_address(self):
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
        member.email_verification_code = Member.get_number(50)
        member.phone_verification_code = Member.get_number(5, True)
        member.save()
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.member.save()