from django.test import TestCase
from rest_framework.test import APIClient
from museum.models import Exhibit, Author, Hall, Collection, Exhibition, Visitor
from datetime import date
from model_bakery import baker

class ExhibitsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        athr = Author.objects.create(
            name = "Шировец",
            surname = "Мария",
            birthdate = "1971-01-23",
            deathdate = "2022-04-15"
        )
        hll = Hall.objects.create(
            name = "Зал современного искусства",
            description = "Зал с произведениями современного искусства",
            location = "Второй этаж, правое крыло"
        )
        cllctn = Collection.objects.create(
            name = "Современное искусство",
            description = "Коллекция современного искусства"
        )
        exhbt = Exhibit.objects.create(
            name = "Цветущая айва",
            author = athr,
            cost = "95000",
            description = "Нежная и трогательная картина, изображающая пробуждение весны. Две части полотна словно две страницы рассказа, показывают красоту цветущей айвы: обильное цветение с левой стороны и одинокий цветок, сияющий на фоне темных листьев, справа.",
            creation_year = 2014,
            collection = cllctn,
            hall = hll
        )
        r = self.client.get('/api/exhibits/')
        data = r.json()
        print(data)

        assert exhbt.name == data[0]['name']
        assert exhbt.cost == data[0]['cost']
        assert exhbt.author.id == data[0]['author']
        assert exhbt.description == data[0]['description']
        assert exhbt.creation_year == data[0]['creation_year']
        assert exhbt.collection.id == data[0]['collection']
        assert exhbt.hall.id == data[0]['hall']
        assert len(data) == 1

    def test_create_exhibit(self):
        athr = baker.make("Author")
        hll = baker.make("Hall")
        cllctn = baker.make("Collection")
        r = self.client.post("/api/exhibits/",{
            "name": "Расвет",
            "author": athr.id,
            "cost": "30000",
            "description": "Последняя каартина художника Полирова",
            "creation_year": 2018,
            "collection": cllctn.id,
            "hall": hll.id
        })


        new_exhibit_id = r.json()['id']

        exhibits = Exhibit.objects.all()
        self.assertEqual(len(exhibits), 1) 

        new_exhibit = Exhibit.objects.filter(id=new_exhibit_id).first()
        assert new_exhibit.name == 'Расвет'
        assert new_exhibit.author == athr
        assert new_exhibit.cost == '30000'
        assert new_exhibit.description == 'Последняя каартина художника Полирова'
        assert new_exhibit.creation_year == 2018
        assert new_exhibit.collection == cllctn
        assert new_exhibit.hall == hll

    def test_delete_exhibit(self):
        exhibits = baker.make("Exhibit", 10)
        r = self.client.get("/api/exhibits/")
        data = r.json()
        assert len(data) == 10

        exhibit_id_to_delete = exhibits[3].id
        self.client.delete(f'/api/exhibits/{exhibit_id_to_delete}/')

        r = self.client.get("/api/exhibits/")
        data = r.json()
        assert len(data) == 9
        
        assert exhibit_id_to_delete not in [i['id'] for i in data]

    def test_update_exhibit(self):
        athr = baker.make("Author")
        hll = baker.make("Hall")
        cllctn = baker.make("Collection")
        exhibits = baker.make("Exhibit", 10)
        exhibit: Exhibit = exhibits[1]

        r = self.client.get(f'/api/exhibits/{exhibit.id}/')
        data = r.json()
        assert data['name'] == exhibit.name

        r = self.client.put(f'/api/exhibits/{exhibit.id}/',{
            "name": "Мечта моя",
            "author": athr.id,
            "cost": "10000",
            "description": "Пупупупупупу",
            "creation_year": 2024,
            "collection": cllctn.id,
            "hall": hll.id
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/exhibits/{exhibit.id}/')
        data = r.json()

        exhibit.refresh_from_db()
        assert data['name'] == "Мечта моя"


class ExhibitionsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        athr = Author.objects.create(
            name = "Шировец",
            surname = "Мария",
            birthdate = "1971-01-23",
            deathdate = "2022-04-15"
        )
        hll = Hall.objects.create(
            name = "Зал современного искусства",
            description = "Зал с произведениями современного искусства",
            location = "Второй этаж, правое крыло"
        )
        cllctn = Collection.objects.create(
            name = "Современное искусство",
            description = "Коллекция современного искусства"
        )
        exhbt = Exhibit.objects.create(
            name = "Цветущая айва",
            author = athr,
            cost = "95000",
            description = "Нежная и трогательная картина, изображающая пробуждение весны. Две части полотна словно две страницы рассказа, показывают красоту цветущей айвы: обильное цветение с левой стороны и одинокий цветок, сияющий на фоне темных листьев, справа.",
            creation_year = 2014,
            collection = cllctn,
            hall = hll
        )

        exhibition = Exhibition.objects.create(
            name = "Выставка современного искусства",
            description = "Выставка работ современных творцов",
            opening_date = "2024-01-01",
            closing_date = "2024-01-31",
        )
        exhibition.exhibits.add(exhbt)
        r = self.client.get('/api/exhibitions/')
        data = r.json()
        print(data)

        assert exhibition.name == data[0]['name']
        assert exhibition.description == data[0]['description']
        assert exhibition.opening_date == data[0]['opening_date']
        assert exhibition.closing_date == data[0]['closing_date']
        assert len(data) == 1
        exhibit_ids = [exhbt.id for exhbt in exhibition.exhibits.all()]
        assert set(exhibit_ids) == set([e['id'] for e in data[0]['exhibits']]) 
    
    def test_create_exhibition(self):
        athr = baker.make("Author")
        hll = baker.make("Hall")
        cllctn = baker.make("Collection")
        exhbt = baker.make("Exhibit")
        r = self.client.post("/api/exhibitions/", {
            "name": 'Выставка современного искусства',
            "description": 'Выставка работ современных творцов',
            "opening_date": '2024-01-01',
            "closing_date": '2024-01-31',
            "exhibits": [exhbt.id]
        })
        
        new_exhibitions_id = r.json()['id']

        exhibits = Exhibit.objects.all()
        self.assertEqual(len(exhibits), 1)

        new_exhibitions = Exhibition.objects.filter(id=new_exhibitions_id).first()
        new_exhibitions.exhibits.add(exhbt) 
        assert new_exhibitions.name == 'Выставка современного искусства'
        assert new_exhibitions.description == 'Выставка работ современных творцов'
        assert new_exhibitions.opening_date == date(2024, 1, 1)
        assert new_exhibitions.closing_date == date(2024, 1, 31)
        assert exhbt in new_exhibitions.exhibits.all()
    
    def test_delete_exhibition(self):
        exhibitions = baker.make("Exhibition", 10)
        r = self.client.get('/api/exhibitions/')
        data = r.json()
        assert len(data) == 10

        exhibition_id_to_delete = exhibitions[3].id
        self.client.delete(f'/api/exhibitions/{exhibition_id_to_delete}/')

        r = self.client.get('/api/exhibitions/')
        data = r.json()
        assert len(data) == 9
        
        assert exhibition_id_to_delete not in [i['id'] for i in data]
    
    def test_update_exhibit(self):
        exhibits = baker.make("Exhibit")
        exhibitions = baker.make("Exhibition", 10)
        exhibition: Exhibition = exhibitions[2]

        r = self.client.get(f'/api/exhibitions/{exhibition.id}/')
        data = r.json()
        assert data['name'] == exhibition.name

        r = self.client.put(f'/api/exhibitions/{exhibition.id}/',{
            "name": "Новиви",
            "description": "Выставка работ новых работ",
            "opening_date": "2024-05-01",
            "closing_date": "2024-05-05",
            
        })
        exhibition.exhibits.add(exhibits)
        assert r.status_code == 200
        r = self.client.get(f'/api/exhibitions/{exhibition.id}/')
        data = r.json()

        exhibition.refresh_from_db()
        assert data['name'] == "Новиви"


class AuthorsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        athr = Author.objects.create(
            name = "Шировец",
            surname = "Мария",
            birthdate = "1971-01-23",
            deathdate = "2022-04-15"
        )
        r = self.client.get('/api/authors/')
        data = r.json()
        print(data)

        assert athr.name == data[0]['name']
        assert athr.surname == data[0]['surname']
        assert athr.birthdate == data[0]['birthdate']
        assert athr.deathdate == data[0]['deathdate']
        assert len(data) == 1
    
    def test_create_author(self):
        r = self.client.post("/api/authors/", {
            "name": 'Полиров',
            "surname": 'Даниил',
            "birthdate": '1920-01-23',
            "deathdate": '2019-01-20'
        })
        
        new_authors_id = r.json()['id']

        authors = Author.objects.all()
        self.assertEqual(len(authors), 1)

        new_authors = Author.objects.filter(id=new_authors_id).first()
        assert new_authors.name == 'Полиров'
        assert new_authors.surname == 'Даниил'
        assert new_authors.birthdate == date(1920, 1, 23)
        assert new_authors.deathdate == date(2019, 1, 20)
    
    def test_delete_author(self):
        authors = baker.make("Author", 10)
        r = self.client.get("/api/authors/")
        data = r.json()
        assert len(data) == 10

        author_id_to_delete = authors[3].id
        self.client.delete(f'/api/authors/{author_id_to_delete}/')

        r = self.client.get("/api/authors/")
        data = r.json()
        assert len(data) == 9
        
        assert author_id_to_delete not in [i['id'] for i in data]
    
    def test_update_author(self):
        authors = baker.make("Author", 10)
        author: Author = authors[1]

        r = self.client.get(f'/api/authors/{author.id}/')
        data = r.json()
        assert data['name'] == author.name

        r = self.client.put(f'/api/authors/{author.id}/',{
            "name": 'Иван',
            "surname": 'Иванов',
            "birthdate": '1950-01-23',
            "deathdate": '2019-01-20'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/authors/{author.id}/')
        data = r.json()

        author.refresh_from_db()
        assert data['name'] == "Иван"


class HallsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        hll = Hall.objects.create(
            name = "Зал современного искусства",
            description = "Зал с произведениями современного искусства",
            location = "Второй этаж, правое крыло"
        )
        r = self.client.get('/api/halls/')
        data = r.json()
        print(data)

        assert hll.name == data[0]['name']
        assert hll.description == data[0]['description']
        assert hll.location == data[0]['location']
        assert len(data) == 1
    
    def test_create_hall(self):
        r = self.client.post("/api/halls/", {
            "name": 'Зал современного искусства',
            "description": 'Зал с произведениями современного искусства',
            "location": 'Второй этаж, правое крыло'
        })
        new_halls_id = r.json()['id']

        hall = Hall.objects.all()
        self.assertEqual(len(hall), 1)

        new_halls = Hall.objects.filter(id=new_halls_id).first()
        assert new_halls.name == 'Зал современного искусства'
        assert new_halls.description == 'Зал с произведениями современного искусства'
        assert new_halls.location == 'Второй этаж, правое крыло'
    
    def test_delete_hall(self):
        halls = baker.make("Hall", 10)
        r = self.client.get("/api/halls/")
        data = r.json()
        assert len(data) == 10

        hall_id_to_delete = halls[3].id
        self.client.delete(f'/api/halls/{hall_id_to_delete}/')

        r = self.client.get("/api/halls/")
        data = r.json()
        assert len(data) == 9
        
        assert hall_id_to_delete not in [i['id'] for i in data]
    
    def test_update_hall(self):
        halls = baker.make("hall", 10)
        hall: Hall = halls[1]

        r = self.client.get(f'/api/halls/{hall.id}/')
        data = r.json()
        assert data['name'] == hall.name

        r = self.client.put(f'/api/halls/{hall.id}/',{
            "name": 'Зал ренессанса',
            "description": 'Зал, где представлены произведения искусства эпохи Возрождения.',
            "location": 'Первый этаж, левое крыло'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/halls/{hall.id}/')
        data = r.json()

        hall.refresh_from_db()
        assert data['name'] == "Зал ренессанса"


class CollectionsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        cllctn = Collection.objects.create(
            name = "Современное искусство",
            description = "Коллекция современного искусства"
        )
        r = self.client.get('/api/collections/')
        data = r.json()
        print(data)

        assert cllctn.name == data[0]['name']
        assert cllctn.description == data[0]['description']
        assert len(data) == 1
    
    def test_create_collection(self):
        r = self.client.post("/api/collections/", {
            "name": 'Современное искусство',
            "description": 'Коллекция современного искусства',
        })
        new_collections_id = r.json()['id']

        collection = Collection.objects.all()
        self.assertEqual(len(collection), 1)

        new_collections = Collection.objects.filter(id=new_collections_id).first()
        assert new_collections.name == 'Современное искусство'
        assert new_collections.description == 'Коллекция современного искусства'
    
    def test_delete_collection(self):
        collections = baker.make("Collection", 10)
        r = self.client.get("/api/collections/")
        data = r.json()
        assert len(data) == 10

        collection_id_to_delete = collections[3].id
        self.client.delete(f'/api/collections/{collection_id_to_delete}/')

        r = self.client.get("/api/collections/")
        data = r.json()
        assert len(data) == 9
        
        assert collection_id_to_delete not in [i['id'] for i in data]
    
    def test_update_collection(self):
        collections = baker.make("collection", 10)
        collection: Collection = collections[1]

        r = self.client.get(f'/api/collections/{collection.id}/')
        data = r.json()
        assert data['name'] == collection.name

        r = self.client.put(f'/api/collections/{collection.id}/',{
            "name": 'Живая история',
            "description": 'Коллекция,  запечатлевающая  ритм современной жизни. Работы  художников,  реагирующих  на  изменения,  влияющие  на  наше  общество,  на  себя  и  на  мир  вокруг',
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/collections/{collection.id}/')
        data = r.json()

        collection.refresh_from_db()
        assert data['name'] == "Живая история"


# class VisitorsViewsetTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
    
#     def test_get_list(self):
#         vstr = Visitor.objects.create(
#             name = "Современное искусство",
#             description = "Коллекция современного искусства"
#         )
#         r = self.client.get('/api/vs/')
#         data = r.json()
#         print(data)

#         assert cllctn.name == data[0]['name']
#         assert cllctn.description == data[0]['description']
#         assert len(data) == 1
    
#     def test_create_collection(self):
#         r = self.client.post("/api/collections/", {
#             "name": 'Современное искусство',
#             "description": 'Коллекция современного искусства',
#         })
#         new_collections_id = r.json()['id']

#         collection = Collection.objects.all()
#         self.assertEqual(len(collection), 1)

#         new_collections = Collection.objects.filter(id=new_collections_id).first()
#         assert new_collections.name == 'Современное искусство'
#         assert new_collections.description == 'Коллекция современного искусства'
    
#     def test_delete_collection(self):
#         collections = baker.make("Collection", 10)
#         r = self.client.get("/api/collections/")
#         data = r.json()
#         assert len(data) == 10

#         collection_id_to_delete = collections[3].id
#         self.client.delete(f'/api/collections/{collection_id_to_delete}/')

#         r = self.client.get("/api/collections/")
#         data = r.json()
#         assert len(data) == 9
        
#         assert collection_id_to_delete not in [i['id'] for i in data]
    
#     def test_update_collection(self):
#         collections = baker.make("collection", 10)
#         collection: Collection = collections[1]

#         r = self.client.get(f'/api/collections/{collection.id}/')
#         data = r.json()
#         assert data['name'] == collection.name

#         r = self.client.put(f'/api/collections/{collection.id}/',{
#             "name": 'Живая история',
#             "description": 'Коллекция,  запечатлевающая  ритм современной жизни. Работы  художников,  реагирующих  на  изменения,  влияющие  на  наше  общество,  на  себя  и  на  мир  вокруг',
#         })
#         assert r.status_code == 200
#         r = self.client.get(f'/api/collections/{collection.id}/')
#         data = r.json()

#         collection.refresh_from_db()
#         assert data['name'] == "Живая история"