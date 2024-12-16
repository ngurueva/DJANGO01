from rest_framework import serializers

from museum.models import Exhibit, Author, Hall, Collection, Exhibition, Visitor

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = "__all__"

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"

class ExhibitSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()) 
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())
    
    class Meta:
        model = Exhibit
        fields = "__all__"




class ExhibitionSerializer(serializers.ModelSerializer):
  exhibits = serializers.PrimaryKeyRelatedField(many=True, queryset=Exhibit.objects.all())

  class Meta:
    model = Exhibition
    fields = '__all__'


class VisitorSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)

    class Meta:
        model = Visitor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'exhibition', 'user']  # тут просто юзера добавил

