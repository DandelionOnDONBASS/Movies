from rest_framework import serializers

from movies.models import *


class FilretReviewSerializer(serializers.ListSerializer):
    '''Фильтр коментариев, только parent'''
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)
    

class RecursiveSerializer(serializers.Serializer):
    '''Сериализатор для children'''
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MovieListSerializer(serializers.ModelSerializer):
    '''Список фильмов'''
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category','year')



class ReviewCreateSerializer(serializers.ModelSerializer):
    '''Добавление отзыва'''
    class Meta:
        model = Reviews
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    '''Отзывы'''
    children = RecursiveSerializer(many=True)
    
    class Meta:
        list_serializer_class = FilretReviewSerializer
        model = Reviews
        fields = ('id','name', 'text','children')


class ActorListSerializer(serializers.ModelSerializer):
    '''Актеры и режиссеры'''
    class Meta:
        model = Actors
        fields = ('id', 'name', 'image')

class ActorDetailSerializer(serializers.ModelSerializer):
    '''Актер или режиссер'''
    class Meta:
        model = Actors
        fields = '__all__'

class MovieDetailSerializer(serializers.ModelSerializer):
    '''Полное описание фильма'''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewsSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateReatingSerializer(serializers.ModelSerializer):
    '''Добавление рейтинга'''
    class Meta:
        model = Rating
        fields = ('star', 'movie')


    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
    



