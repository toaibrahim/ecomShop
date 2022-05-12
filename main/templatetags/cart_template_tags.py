
from django import template
from main.models import Order,Wishlisted

register = template.Library()

@register.filter
def user_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user = user,ordered=False)
        if qs.exists():
            return qs[0].items.count()

    return 0


@register.filter
def user_wishlist_count(user):
    if user.is_authenticated:
        qs = Wishlisted.objects.filter(user = user)
        if qs.exists():
            return qs[0].items.count()

    return 0