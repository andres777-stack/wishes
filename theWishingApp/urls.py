from django.urls import path
from . import views

app_name = 'wishes'

#wishes/
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('granted/<int:id>', views.granted, name='granted'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('liked/<int:id>', views.liked, name='liked'),
]

