from django.db import models
from django.contrib.auth.models import User


# Продукт с владельцем
class Product(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')


# Урок используемый в продуктах
class Lesson(models.Model):
	title = models.CharField(max_length=50)
	link = models.TextField(null=True, blank=True)
	duration = models.PositiveIntegerField(default=0)
	product = models.ManyToManyField(Product, related_name='lessons')


# Назначение доступа студентов к продуктам
class Availability(models.Model):
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)


# Статус просмотра уроков студентами
class View(models.Model):
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='view')
	student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='view')
	viewed = models.PositiveIntegerField(default=0)
	status = models.BooleanField(default=False)
