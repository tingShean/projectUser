from django.db import models


# Create your models here.
class UserManagers(models.Model):
    uid = models.IntegerField(primary_key=True)
    account = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    create_time = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_managers'


class Admin(models.Model):
    uid = models.IntegerField()
    manage_lv = models.IntegerField()

    class Meta:
        db_table = 'admin'


class UserAuthorize(models.Model):
    uid = models.IntegerField()
    page = models.CharField(max_length=20)
    authorize = models.CharField(max_length=4)

    class Meta:
        db_table = 'user_authorize'


class PageName(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'page_name'
