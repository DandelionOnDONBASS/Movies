from django.urls import path, include, re_path
from . import views
from .views import MovieListView
from .yasg import urlpatterns as doc_urls

app_name = 'api'

urlpatterns = [
    path('movies/', MovieListView.as_view()), 
    path('movie/<int:pk>/', views.MovieDetailView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('actors/', views.ActorListView.as_view()),
    path('review/<int:pk>/', views.ReviewsView.as_view()),
    path('actor/<int:pk>/', views.ActorDetailView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls