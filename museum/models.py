from django.db import models
from django.core.exceptions import ValidationError

class Author(models.Model):
    name = models.TextField("Имя")
    surname = models.TextField("Фамилия")
    birthdate = models.DateField("Дата рождения", null=True)
    deathdate = models.DateField("Дата смерти", null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="authors") 
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
    def __str__(self) -> str:
        return self.name + " " + self.surname

class Collection(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание", null=True)

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

    def __str__(self) -> str:
        return self.name

class Hall(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание", null=True)
    location = models.TextField("Местоположение", null=True)
    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"
    def __str__(self) -> str:
        return self.name

class Exhibit(models.Model):
    name = models.TextField("Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="exhibits", verbose_name="Автор", null=True)  # Связь с автором
    cost = models.TextField("Стоимость", null=True)
    description = models.TextField("Описание", null=True)
    creation_year = models.IntegerField("Год создания", null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="exhibits", null=True, verbose_name="Коллекция")  # Связь с коллекцией
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="exhibits", verbose_name="Холл", null=True)  # Связь с залом
# добавим ImageField, в upload_to указываем папку куда загружать файл
    picture = models.ImageField("Изображение", null=True, blank=True, upload_to="exhibits")  # blank=True позволяет не вставлять картинку
    class Meta:
        verbose_name = "Экспонат"
        verbose_name_plural = "Экспонаты"
    def __str__(self) -> str:
        return self.name

class Exhibition(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание", null=True)
    opening_date = models.DateField("Дата открытия", null=True)
    closing_date = models.DateField("Дата закрытия", null=True)
    exhibits = models.ManyToManyField(Exhibit, related_name="exhibitions", verbose_name="Экспонаты")  # Связь многие-ко-многим с экспонатами
    class Meta:
        verbose_name = "Выставка"
        verbose_name_plural = "Выставки" 
        
class Visitor(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Email", null=True, blank=True)
    phone_number = models.CharField("Телефон", max_length=20, null=True, blank=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name="visitors", null=True, verbose_name="Выставка") 
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"