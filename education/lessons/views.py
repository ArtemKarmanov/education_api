from django.contrib.auth.models import User

from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Product
from .serializers import LessonSerializer, MetricsProductSerializer, LessonsProductSerializer


@extend_schema(
	summary='Список уроков доступных студенту.',
	parameters=[
		OpenApiParameter(
			name='user_id',
			location=OpenApiParameter.QUERY,
			description='Идентификатор студента',
			required=True,
			type=int
		)
	]
)
class LessonsAPIView(ListAPIView):
	"""
	Список уроков доступных студенту.
	"""
	serializer_class = LessonSerializer

	def get_queryset(self):
		# Параметры из GET-запроса
		user_id = self.request.query_params.get('user_id')

		# Проверка на доступность продукта и существование студента
		try:
			user = User.objects.get(id=user_id)
			products = Product.objects.filter(students=user_id)
		except Exception:
			return None

		# Список уроков с добавлением информации по уроку для определенного студента
		result = list()
		for product in products:
			for lesson in product.lessons.all():
				view, created = lesson.views.get_or_create(student=user)
				lesson.userInfo = view
				result.append(lesson)

		return result


@extend_schema(
	summary='Продукт с уроками доступный студенту.',
	parameters=[
		OpenApiParameter(
			name='user_id',
			location=OpenApiParameter.QUERY,
			description='Идентификатор студента',
			required=True,
			type=int
		),
		OpenApiParameter(
			name='product_id',
			location=OpenApiParameter.QUERY,
			description='Идентификатор продукта',
			required=True,
			type=int
		)
	]
)
class ProductAPIView(ListAPIView):
	"""
	Продукт с уроками доступный студенту.
	"""
	serializer_class = LessonsProductSerializer

	def get_queryset(self):
		# Параметры из GET-запроса
		user_id = self.request.query_params.get('user_id')
		product_id = self.request.query_params.get('product_id')

		# Поиск товара по идентификатору и проверка принадлежности студенту
		try:
			product = Product.objects.get(id=product_id, students=user_id)
		except Exception:
			return None

		# Список уроков с добавлением информации по уроку для определенного студента
		result = list()
		for lesson in product.lessons.all():
			view = lesson.views.get(student=user_id)
			lesson.userInfo = view
			result.append(lesson)

		return result


@extend_schema(
	summary='Статистика по всем продуктам.'
)
class MetricsAPIView(ListAPIView):
	"""
	Представление статистики по всем продуктам с REST API.
	"""
	queryset = Product.objects.all()
	serializer_class = MetricsProductSerializer

