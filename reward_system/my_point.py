from .models import Reward

def count_point(request, order):
    reward = Reward.objects.get_or_create(member=request.user.member)[0]
    if reward:
        items = order.item_in_order.all()
        points = [(o.quantity*o.product.point) for o in items]
        reward.current_point += int(round(order.total_price * 0.1 /100))
        reward.save()