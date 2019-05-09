from django import template

register = template.Library()

@register.filter(name='to_range')
def to_range(value):
    return [i for i in range(value)]

@register.filter(name='sub')
def sub(old, value):
    sub = old-value
    return sub

@register.filter(name='user_name')
def user_name(array,index):
    return array[index]['user_name'].capitalize()

@register.filter(name='amount')
def amount(array,index):
    return array[index]['amount']

