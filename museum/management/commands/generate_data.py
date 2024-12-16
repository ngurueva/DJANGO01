from django.core.management.base import BaseCommand
from faker import Faker
from museum.models import Author, Collection, Hall, Exhibit, Exhibition, Visitor
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

class Command(BaseCommand):
  def handle(self, *args, **options):
    fake = Faker(['ru_RU'])

    num_authors = 1000
    num_collections = 1000
    num_halls = 1000
    num_exhibits = 1000
    num_exhibitions = 1000
    num_visitors = 1000

    self.create_fake_data(Author, num_authors, {
      'name': fake.first_name,
      'surname': fake.last_name,
      'birthdate': lambda: fake.date_between(start_date='-80y', end_date='-20y'),
      'deathdate': lambda: fake.date_between(start_date='-80y', end_date='-20y') if fake.boolean() else None,
      'picture': lambda: None, 
    })

    self.create_fake_data(Collection, num_collections, {
      'name': fake.sentence,
      'description': lambda: fake.paragraph(),
    })

    self.create_fake_data(Hall, num_halls, {
      'name': fake.word,
      'description': lambda: fake.paragraph(),
      'location': lambda: fake.street_address(),
    })


    authors = Author.objects.all()
    collections = Collection.objects.all()
    halls = Hall.objects.all()

    self.create_fake_data(Exhibit, num_exhibits, {
      'name': fake.sentence,
      'author': lambda: random.choice(authors) if authors else None,
      'cost': lambda: str(random.randint(100, 10000)),
      'description': lambda: fake.paragraph(),
      'creation_year': lambda: random.randint(1800, 2023),
      'collection': lambda: random.choice(collections) if collections else None,
      'hall': lambda: random.choice(halls) if halls else None,
      'picture': lambda: None, 
    })

    exhibits = Exhibit.objects.all()
    self.create_fake_data(Exhibition, num_exhibitions, {
      'name': fake.sentence,
      'description': lambda: fake.paragraph(),
      'opening_date': lambda: fake.date_between(start_date='-2y', end_date='-1y'),
      'closing_date': lambda: fake.date_between(start_date='-1y', end_date='today'),
      'exhibits': lambda: random.sample(list(exhibits), random.randint(1, min(len(exhibits), 5))), 
    })


    users = User.objects.all()
    exhibitions = Exhibition.objects.all()

    self.create_fake_data(Visitor, num_visitors, {
      'first_name': fake.first_name,
      'last_name': fake.last_name,
      'email': fake.email,
      'phone_number': fake.phone_number,
      'exhibition': lambda: random.choice(exhibitions) if exhibitions else None,
      'user': lambda: random.choice(users),
    })


  def create_fake_data(self, model, num_objects, field_data):
    for _ in range(num_objects):
        kwargs = {field: field_data[field]() if callable(field_data[field]) else field_data[field]
             for field in field_data if field != 'exhibits'}

        instance = model.objects.create(**kwargs)
        if model == Exhibition:
          exhibits = random.sample(list(Exhibit.objects.all()), random.randint(1, min(len(Exhibit.objects.all()), 5)))
          instance.exhibits.set(exhibits)