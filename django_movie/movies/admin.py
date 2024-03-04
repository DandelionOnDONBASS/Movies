from django.contrib import admin

from django import forms
from .models import *
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание',widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание',widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id' ,'name', 'url', )
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('email', 'name')

class MovieShortsInline(admin.TabularInline):
    model = MovieShorts
    extra = 1
    readonly_fields = ('get_image',)
    fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"

@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ('title', 'url', 'category','draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    form = MovieAdminForm
    inlines = [MovieShortsInline, ReviewInline, ]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    filter_horizontal = ('genres',)
    fields = ( 'title','trailer', ('tagline', 'description'), ('poster','year','country'), ('directors', 'actors', 'genres'),
               ('world_premiere','budget','fees_in_usa','fees_in_world'), 'category', 'url','draft')






@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'movie','parent',)
    list_filter = ('movie',)
    readonly_fields = ('name',)
    # search_fields = ('title', 'category__name')


@admin.register(Actors)
class ActorAdmin(TranslationAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"

@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('name', 'url')
    list_filter = ('name',)


@admin.register(MovieShorts)
class MovieShotsAdmin(TranslationAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)

@admin.register(Rating)
class RetingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'star', 'movie')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')




