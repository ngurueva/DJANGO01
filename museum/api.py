from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets, serializers

from museum.models import Exhibit
from museum.serializers import ExhibitSerializer
from museum.models import Author
from museum.serializers import AuthorSerializer
from museum.models import Hall
from museum.serializers import HallSerializer
from museum.models import Collection
from museum.serializers import CollectionSerializer
from museum.models import Exhibition
from museum.serializers import ExhibitionSerializer
from museum.models import Visitor
from museum.serializers import VisitorSerializer

from rest_framework.decorators import action
from rest_framework.response import Response


from django.db.models import Avg, Count, Max, Min


class ExhibitsViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    
):
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.IntegerField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Exhibit.objects.aggregate(
            count = Count("*"), 
            avg = Avg("id"),
            max = Max("id"),
            min = Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class AuthorsViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.IntegerField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Author.objects.aggregate(
            count = Count("*"), 
            avg = Avg("id"),
            max = Max("id"),
            min = Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class HallsViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    
):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.IntegerField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Hall.objects.aggregate(
            count = Count("*"), 
            avg = Avg("id"),
            max = Max("id"),
            min = Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class CollectionsViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    
):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.IntegerField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Collection.objects.aggregate(
            count = Count("*"), 
            avg = Avg("id"),
            max = Max("id"),
            min = Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class ExhibitionsViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    
):
    queryset = Exhibition.objects.all()
    serializer_class = ExhibitionSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.IntegerField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Exhibition.objects.aggregate(
            count = Count("*"), 
            avg = Avg("id"),
            max = Max("id"),
            min = Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

# class VisitorsViewset(
#     mixins.ListModelMixin, 
#     mixins.CreateModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     GenericViewSet
    
# ):
#     queryset = Visitor.objects.all()
#     serializer_class = VisitorSerializer

#     def get_queryset(self):
#         qs = super().get_queryset()
        
#         # фильтруем по текущему юзеру
#         qs = qs.filter(user=self.request.user)

#         return qs


class VisitorsViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return qs 
            else:
                qs = qs.filter(user=self.request.user)
        return qs
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.IntegerField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Visitor.objects.aggregate(
            count = Count("*"), 
            avg = Avg("id"),
            max = Max("id"),
            min = Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)


class UserProfileViewSet(GenericViewSet):
    @action(url_path="info", detail=False, methods=["GET"])
    def get_url(self, request, *args, **kwargs):
        user = request.user
        data = {
            "is_authenticated": user.is_authenticated
        }
        if user.is_authenticated:
            data.update({
                "is_superuser": user.is_superuser,
                "name": user.username
                })
        return Response(data)
    

    
