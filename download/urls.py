from django.urls import path
from . import views



urlpatterns = [
    path('', views.ytd, name='ytd'),
    path('download/', views.download_page, name="download"),
    path('download/<res>/', views.success, name="success")
]