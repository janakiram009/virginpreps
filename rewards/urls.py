from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.reward_list, name='reward_list'),
    path('detail/<int:id>/', views.reward_detail, name='reward_detail'),
    path('create/', views.reward_create, name='reward_create'),
    path('update/<int:id>/', views.reward_update, name='reward_update'),
    path('delete/<int:id>/', views.reward_delete, name='reward_delete'),
]
