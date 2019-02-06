from purchase_order.models import PurchaseOrder
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def check_current_purcashing(user, reward):
    now = datetime.datetime.now()
    reward = reward
    orders = PurchaseOrder.objects.filter(user=user, is_verified=True, is_valid=True,
        created_date__year=now.year, created_date__month=now.month)
    return sum([o.total_price for o in orders])

def check_last_month_purcashing(user, reward):
    prev= date.today().replace(day=1) + relativedelta(months=-1)
    reward = reward
    orders = PurchaseOrder.objects.filter(user=user, is_verified=True, is_valid=True,
        created_date__year=prev.year, created_date__month=prev.month)
    return sum([o.total_price for o in orders])

def check_last_two_month_purcashing(user, reward):
    prev_two = date.today().replace(day=1) + relativedelta(months=-2)
    reward = reward
    orders = PurchaseOrder.objects.filter(user=user, is_verified=True, is_valid=True,
        created_date__year=prev_two.year, created_date__month=prev_two.month)
    return sum([o.total_price for o in orders])

def check_purchasing_bonus(request):
    member = request.user.member
    reward = member.reward
    current_purcashing = check_current_purcashing(request.user, reward)
    last_month_purcashing = check_last_month_purcashing(request.user, reward)
    last_two_month_purcashing = check_last_two_month_purcashing(request.user, reward)
    target = member.get_level()['TARGET']
    bonus = member.get_level()['PURCHASING_BONUS']
    if current_purcashing >= target and \
        last_month_purcashing >= target and \
        last_two_month_purcashing >= target  :
        reward.bonus_purchasing = bonus
        reward.save()
        is_achieved = True
        invalidate_previous_order_bonus(request)
    else:
        is_achieved = False

    return {'is_achieved':is_achieved}


def invalidate_previous_order_bonus(request):
    prev_two = date.today().replace(day=1) + relativedelta(months=-2)
    orders = PurchaseOrder.objects.filter(user=request.user, is_verified=True, is_valid=True,
        created_date__gte=prev_two)
    for order in orders:
        order.is_valid = False
        order.save()
