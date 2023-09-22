from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers

from .models import Product, Lesson, View


class ViewLessonSerializer(serializers.ModelSerializer):
	"""
	Сериализация статуса просмотра урока с датой последнего просмотра.
	"""
	class Meta:
		model = View
		fields = (
			'viewed',
			'status',
			'lastViewed'
		)


class LessonsProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация уроков с датой последнего просмотра.
	"""
	userInfo = ViewLessonSerializer()

	class Meta:
		model = Lesson
		fields = (
			'id',
			'title',
			'link',
			'duration',
			'userInfo'
		)


class ViewSerializer(serializers.ModelSerializer):
	"""
	Сериализация статуса просмотра уроков.
	"""

	class Meta:
		model = View
		fields = (
			'viewed',
			'status',
		)


class LessonSerializer(serializers.ModelSerializer):
	"""
	Сериализация списка уроков.
	"""
	userInfo = ViewSerializer()

	class Meta:
		model = Lesson
		fields = (
			'id',
			'title',
			'link',
			'duration',
			'userInfo'
		)


class MetricsProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация статистики по продуктам.
	"""
	countViewed = serializers.SerializerMethodField()
	totalViewed = serializers.SerializerMethodField()
	countStudents = serializers.SerializerMethodField()
	sales = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = (
			'id',
			'name',
			'countViewed',
			'totalViewed',
			'countStudents',
			'sales'
		)

	def get_countViewed(self, obj):
		"""
		Кол-во просмотренных уроков у продукта.

		:param obj: Продукт
		:return: count_viewed
		"""
		count_viewed = obj.lessons.filter(views__status=True).count()

		return count_viewed

	def get_totalViewed(self, obj):
		"""
		Суммарное время потраченное на просмотр уроков у продукта.

		:param obj: Продукт
		:return: total_viewed
		"""
		total_viewed = obj.lessons.aggregate(Sum('views__viewed'))['views__viewed__sum']

		return total_viewed

	def get_countStudents(self, obj):
		"""
		Кол-во студентов занимающихся у продукта.

		:param obj: Продукт
		:return: count_students
		"""
		count_students = obj.students.count()

		return count_students

	def get_sales(self, obj):
		"""
		Процент приобретения продукта в отношении ко всем студентам.

		:param obj: Продукт
		:return: sales
		"""
		users = User.objects.count()
		count_students = self.get_countStudents(obj)
		sales = round(count_students / users * 100, 2)
		return sales
