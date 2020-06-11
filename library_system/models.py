from django.db import models
import mongoengine


# Create your models here.
class Book(mongoengine.Document):
    isbn = mongoengine.StringField(max_length=30, primary_key=True)
    name = mongoengine.StringField(max_length=20)
    author = mongoengine.StringField(max_length=20)
    press = mongoengine.StringField(max_length=20)
    category = mongoengine.StringField(max_length=6)
    count = mongoengine.IntField()
    press_date = mongoengine.DateField()
    buy_data = mongoengine.StringField(max_length=40)
    price = mongoengine.DecimalField()


class BookCopy(mongoengine.Document):
    # id = mongoengine.StringField(max_length=30, primary_key=True)
    isbn = mongoengine.StringField(max_length=30)
    entry_time = mongoengine.DateField()
    col_sites = mongoengine.StringField(max_length=4)
    if_lend = mongoengine.BooleanField()
    if_book = mongoengine.BooleanField()
    book_username = mongoengine.StringField(max_length=15)


class Reader(mongoengine.Document):
    # id = mongoengine.StringField(max_length=8, primary_key=True)
    username = mongoengine.StringField(max_length=15)
    password = mongoengine.StringField(max_length=15)
    if_lend = mongoengine.BooleanField()
    lend_num = mongoengine.IntField()
    phone = mongoengine.StringField(max_length=12)
    email = mongoengine.StringField(max_length=20)
    name = mongoengine.StringField(max_length=20)
    class_ = mongoengine.StringField(max_length=8)
    maj = mongoengine.StringField(max_length=20)


class Manager(mongoengine.Document):
    # id = mongoengine.StringField(max_length=10, primary_key=True)
    username = mongoengine.StringField(max_length=20)
    password = mongoengine.StringField(max_length=15)
    name = mongoengine.StringField(max_length=10)
    sex = mongoengine.StringField(max_length=1, choices=["男", "女"])
    date = mongoengine.DateField()
    job = mongoengine.StringField(max_length=2, choices=["图书", "系统"])


class CollisionSite(mongoengine.Document):
    name = mongoengine.StringField(max_length=20)
    address = mongoengine.StringField(max_length=30)
    phone = mongoengine.StringField(max_length=13)
    description = mongoengine.StringField(max_length=100)


class LeadInfo(mongoengine.Document):
    rid = mongoengine.StringField(max_length=30)
    bid = mongoengine.StringField(max_length=30)
    lend_date = mongoengine.DateField()
    back_date = mongoengine.DateField()
    backed = mongoengine.BooleanField()
    relend_times = mongoengine.IntField(choices={0, 1, 2})
    relend_ability = mongoengine.BooleanField()


class BookInfo(mongoengine.Document):
    rid = mongoengine.StringField(max_length=30)
    bid = mongoengine.StringField(max_length=30)
    used = mongoengine.BooleanField()
    lend_date = mongoengine.DateField()


class Comment(mongoengine.Document):
    username = mongoengine.StringField(max_length=30)
    isbn = mongoengine.StringField(max_length=30)
    content = mongoengine.StringField(max_length=140)
    date = mongoengine.DateTimeField()

