from django.db import models


# Create your models here.
class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    account = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


class Cashflow(models.Model):
    uid = models.IntegerField()
    cost = models.IntegerField()
    have_stone = models.IntegerField()
    cost_type = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cashflow'
