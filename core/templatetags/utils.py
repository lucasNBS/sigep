from django import template


register = template.Library()

@register.filter
def get_permission_for_user(inst, user):
    return inst.get_permission(user)

@register.filter
def starts_with(value, arg):
    return value.startswith(arg)

@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    request = context["request"]
    query = request.GET.copy()

    for key, value in kwargs.items():
        if value is None:
            query.pop(key, None)
        else:
            query[key] = value

    return query.urlencode()
