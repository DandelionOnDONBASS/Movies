from modeltranslation.translator import register, TranslationOptions
from .models import Category, Actors, Movie, Genre, MovieShorts


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Actors)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(MovieShorts)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')