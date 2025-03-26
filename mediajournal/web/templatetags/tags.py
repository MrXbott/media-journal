from django import template

register = template.Library()

@register.filter()
def item(d, key):
    return d.get(key)


@register.filter()
def set_attrs(field, attrs_string:str):
    attrs = {}
    try:
        # to do: normal parsing
        for ss in attrs_string.split(','):
            ss_kv = ss.strip().split(':')
            attrs.update({ss_kv[0]: ss_kv[1]})
    except:
        raise Exception('Can\'t parse attrs string')

    return field.as_widget(attrs=attrs)