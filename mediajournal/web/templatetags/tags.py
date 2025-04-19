from django import template

from articles.models import Article, Category
from news.models import News

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


@register.inclusion_tag('sidebar.html')
def render_sidebar():
    return {
        'latest_news': News.objects.filter(status=News.Status.PUBLISHED).order_by('-published')[:5],
        'latest_articles': Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5],
        'categories': Category.objects.filter(parent=None).order_by('name')
    }