from django.contrib import admin

# Register your models here.
from museum.models import Author
from museum.models import Hall
from museum.models import Collection
from museum.models import Exhibit
from museum.models import Exhibition
from museum.models import Visitor


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'creation_year']
@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'opening_date', 'closing_date']
@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'exhibition']

