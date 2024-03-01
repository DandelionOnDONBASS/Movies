# from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Movie, Category,Actors, Genre, Rating,Contact
from django.views.generic.base import View
from .forms import ReviewForm, RatingForm
from django.http import JsonResponse, HttpResponse
# from django.contrib.auth.views import LoginView
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# class MyLoginView(LoginView):
#     template_name = 'movies/users/login.html'
#     form_class = UserLoginForm

    
# class UserRegisterView(CreateView):
#     model = AbstractUser
#     template_name = 'movies/users/register.html'
#     form_class = UserRegisterForm


    


class GenreYear:
    def get_ganres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=True)



class MoviesView(GenreYear,ListView):
    '''Список фильмов'''
    model = Movie
    queryset = Movie.objects.filter(draft=False).order_by('id')
    paginate_by = 1

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories'] = Category.objects.all()
        return context






class MovieDitailView(GenreYear,DetailView):
    '''Полное описание фильма'''
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args,**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, 'movies/movie_detail.html', {'movie': movie})


class AddReview(View):
    '''Отзывы'''
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie_id = pk
            form.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class ActorVew(GenreYear,DetailView):
    model = Actors
    template_name = 'movies/actor.html'
    slug_field = 'name_ru'



class FilterMovieView(ListView):
    paginate_by = 1
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genres'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context['genres'] = ''.join([f"genres={x}&" for x in self.request.GET.getlist('genres')])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    paginate_by = 1

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genres"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip


    def post(self, request, pk):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip = self.get_client_ip(request),
                movie_id=pk,
                defaults={'star_id': int(request.POST.get("star"))}
            )
        else:
            print('neeee')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    


class Search(ListView):
    paginate_by = 1
    def get_queryset(self):
        print(f"------{self.request.path}")
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        print(context)
        return context


class ContactView(View):
    def post(self, request):
        print(request.POST)
        contact = Contact.objects.update_or_create(email = request.POST.get('Email'))
        return redirect(request.META.get('HTTP_REFERER', '/'))
        