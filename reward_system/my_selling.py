from purchase_order.models import PurchaseOrderItem
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def check_current_selling(user, reward):
    now = datetime.datetime.now()
    reward = reward
    order_items = PurchaseOrderItem.objects.filter(
        product_referal=user.member, 
        purchase_order__is_verified=True, 
        is_valid=True,
        purchase_order__created_date__year=now.year, 
        purchase_order__created_date__month=now.month)
    return sum([(o.product.price*o.quantity) for o in order_items])

def check_selling_bonus(request):
    member = request.user.member
    reward = member.reward
    current_selling = check_current_selling(request.user, reward)
    target = member.get_level()['TARGET']
    bonus = member.get_level()['SELLING_BONUS']
    if current_selling >= target :
        reward.bonus_selling = bonus
        reward.save()
        is_achieved = True
        invalidate_previous_order_bonus(request)
    else:
        is_achieved = False

    return {'is_achieved':is_achieved}


def invalidate_previous_order_bonus(request):
    order_items = PurchaseOrderItem.objects.filter(
        product_referalr=user.member, 
        purchase_order__is_verified=True, 
        is_valid=True,
        purchase_order__created_date__year=now.year, 
        purchase_order__created_date__month=now.month)
    for order in order_items:
        order.is_valid = False
        order.save()
