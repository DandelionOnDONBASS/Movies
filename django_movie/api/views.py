from rest_framework.response import Response
from rest_framework.views import APIView
from .service import get_client_ip, MovieFilter
from movies.models import Movie, Reviews
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from rest_framework.pagination import PageNumberPagination

class OneItemPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'  # параметр запроса для установки количества элементов на странице
    max_page_size = 1000  # максимальное количество элементов на странице

class MovieListView(generics.ListAPIView):
    '''Вывод всех фильмов
    http://127.0.0.1:8000/api/v1/movies/?year=2002,2004,2009&genres=Боевик'''
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieListSerializer
    pagination_class = OneItemPagination
    # filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]
    


class MovieDetailView(generics.RetrieveAPIView):
    '''Вывод конкретного фильма'''
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
    

class ReviewCreateView(generics.CreateAPIView):
    '''Добавление отзыва к фильму'''
    serializer_class = ReviewCreateSerializer
      
    

class ReviewsView(generics.RetrieveAPIView):
    '''Вывод отзывов к фильму'''
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    
    


class AddStarRatingView(generics.CreateAPIView):
    '''Добавление рейтинга фильму'''
    serializer_class = CreateReatingSerializer
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorListView(generics.ListAPIView):
    '''Вывод всех актеров'''
    queryset = Actors.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    '''Вывод конкретного актера'''
    queryset = Actors.objects.all()
    serializer_class = ActorDetailSerializer 