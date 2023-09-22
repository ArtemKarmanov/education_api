from rest_framework.generics import ListAPIView

from .models import Product
from .serializers import LessonSerializer, MetricsProductSerializer, LessonsProductSerializer

from django.contrib.auth.models import User


class LessonsAPIView(ListAPIView):
	serializer_class = LessonSerializer

	def get_queryset(self):
		user_id = self.request.query_params.get('user_id')

		user = User.objects.get(id=user_id)

		products = Product.objects.filter(students=user_id)

		result = list()

		for product in products:
			for lesson in product.lessons.all():
				view, created = lesson.views.get_or_create(student=user)
				lesson.userInfo = view
				result.append(lesson)

		return result


class ProductAPIView(ListAPIView):
	serializer_class = LessonsProductSerializer

	def get_queryset(self):
		user_id = self.request.query_params.get('user_id')
		product_id = self.request.query_params.get('product_id')

		product = Product.objects.get(id=product_id, students=user_id)

		result = list()

		for lesson in product.lessons.all():
			view = lesson.views.get(student=user_id)
			lesson.userInfo = view
			result.append(lesson)

		return result


class MetricsAPIView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = MetricsProductSerializer

