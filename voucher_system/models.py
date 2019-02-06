from django.db import models

class Voucher(models.Model):
    DISCOUNT_PRODUCT = 0
    DISCOUNT_ONGKIR = 1
    PERCENT_PRODUCT = 2
    PERCENT_ONGKIR = 3
    BONUS_POINT = 4
    CASHBACK = 5

    BENEFIT_TYPE_CHOICES = (
        (DISCOUNT_PRODUCT, 'Diskon Produk'),
        (DISCOUNT_ONGKIR, 'Diskon Ongkir'),
        (PERCENT_PRODUCT, 'Persen Diskon Produk'),
        (PERCENT_ONGKIR, 'Persen Diskon Ongkir'),
        (BONUS_POINT, 'Bonus Poin'),
        (CASHBACK, 'Cashback Pembelian'),
    )

    MINIMAL_SUM = 6
    MAXIMAL_BENEFIT = 7

    CONDITION_TYPE_CHOICES = (
        (MINIMAL_SUM, 'Minimal Pembelian'),
        (MAXIMAL_BENEFIT, 'Batas Maksimal Keuntungan'),
    )
    name = models.CharField(max_length = 200,
            db_index=True,
            help_text="Nama Voucher")
    voucher_code = models.CharField(db_index=True, 
            max_length=12, 
            blank=True,
            help_text="Kode Voucher")
    benefit = models.PositiveSmallIntegerField(choices=BENEFIT_TYPE_CHOICES, help_text="Keuntungan Voucher",default=DISCOUNT_PRODUCT)
    condition = models.PositiveSmallIntegerField(choices=CONDITION_TYPE_CHOICES, help_text="Syarat & Kondisi Voucher", default=MINIMAL_SUM)
    value = models.PositiveIntegerField(help_text="Nilai Keuntungan Voucher", default=0)
    threshold = models.PositiveIntegerField(help_text="Nilai Syarat & Kondisi Voucher", default=0)

    def apply_voucher(self, amount):
        if self.condition == Voucher.DISCOUNT_PRODUCT:
            pass
        elif self.condition == Voucher.DISCOUNT_ONGKIR:
            pass
        elif self.condition == Voucher.PERCENT_PRODUCT:
            pass
        elif self.condition == Voucher.PERCENT_ONGKIR:
            pass
        elif self.condition == Voucher.BONUS_POINT:
            pass
        elif self.condition == Voucher.CASHBACK:
            pass