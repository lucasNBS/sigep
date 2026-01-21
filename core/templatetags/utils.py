from django import template


register = template.Library()

@register.filter
def get_permission_for_user(inst, user):
    return inst.get_permission(user)

@register.filter
def starts_with(value, arg):
    return value.startswith(arg)
