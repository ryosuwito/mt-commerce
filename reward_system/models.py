from django.db import models
from membership.models import Member
from .my_purchasing import check_current_purcashing, check_purchasing_bonus
from .my_selling import check_current_selling, check_selling_bonus

class Reward(models.Model):
    member = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True)
    current_point = models.PositiveIntegerField(blank=True, default=0)
    bonus_purchasing = models.PositiveIntegerField(blank=True, default=0)
    bonus_selling = models.PositiveIntegerField(blank=True, default=0)

    def get_current_purchasing(self):
        return check_current_purcashing(self.member.user, self)
    def get_current_selling(self):
        return check_current_selling(self.member.user, self)
    def get_purchasing_bonus(self, request):
        return check_purchasing_bonus(request)
    def get_selling_bonus(self, request):
        return check_purchasing_bonus(request)
