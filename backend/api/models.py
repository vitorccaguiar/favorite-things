from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=50)

class FavoriteThing(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField(blank=True)
  ranking = models.IntegerField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date = models.DateField(auto_now_add=True)
  modified_date = models.DateField(auto_now=True)

class Metadata(models.Model):
  key = models.CharField(max_length=50)
  type = models.CharField(max_length=50)
  value = models.CharField(max_length=100)
  favorite_thing = models.ForeignKey(FavoriteThing, on_delete=models.CASCADE)

class AuditLog(models.Model):
  related_model_name = models.CharField(max_length=50)
  action_performed = models.CharField(max_length=50)
  created_date = models.DateField(auto_now_add=True)
  favorite_thing =  models.ForeignKey(FavoriteThing, on_delete=models.CASCADE)