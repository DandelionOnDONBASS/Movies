from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MoviesView.as_view(), name='index'),
    # path('registration/', views.UserRegisterView.as_view(), name='register'),
    path('filter/', views.FilterMovieView.as_view(), name='filter'),
    path('filter/page/<int:page>', views.FilterMovieView.as_view(), name='filter'),
    path('search', views.Search.as_view(), name='search'),
    path('search/page/<int:page>', views.Search.as_view(), name='search'),
    path('<slug:slug>/', views.MovieDitailView.as_view(), name='movie_detail'),
    path('page/<int:page>/', views.MoviesView.as_view(), name='paginator'),
    path('add-rating/<int:pk>/', views.AddStarRating.as_view(), name='add_rating'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', views.ActorVew.as_view(), name='actor_detail'),
    path('contact', views.ContactView.as_view(), name='contact'),   
]