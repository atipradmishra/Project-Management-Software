from django import template
from ..models import Dip_Activities

register=template.Library()
def myvalue(ingredients):
 
    decoder = dict(Dip_Activities.MONTH_CHOICES)
    decoded = [decoder[t] for t in ingredients]
    decoded.sort(reverse = True)
    return '\n'.join(decoded)

register.filter('myvalue', myvalue)