
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.null),
    path('root/', views.root),
    # path('int/<int:id>/', views.int),
    path('int/<int:id>/', views.int_view, name='int_view'),
]
