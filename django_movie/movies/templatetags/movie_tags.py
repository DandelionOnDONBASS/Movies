from django import template
from ..models import Category, Movie, Genre

register = template.Library()

@register.simple_tag()
def get_category():
    return Category.objects.all()


@register.simple_tag()
def get_last_movies():
    return Movie.objects.filter(draft=False).order_by('id')[:5]


@register.simple_tag()
def get_movies():
    return Movie.objects.filter(draft=False).order_by('id')



@register.simple_tag()
def get_genre():
    return Genre.objects.all()

