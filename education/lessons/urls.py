from django.urls import path
from .views import LessonsAPIView, ProductAPIView, MetricsAPIView

app_name = 'lessons'

urlpatterns = [
	path('lessons/', LessonsAPIView.as_view(), name='lessons'),
	path('product/', ProductAPIView.as_view(), name='product'),
	path('metrics/', MetricsAPIView.as_view(), name='metrics'),
]