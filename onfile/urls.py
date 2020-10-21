from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('csv/', views.process_csv, name='csv'),
]
