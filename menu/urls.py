from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.MenuCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.MenuCategoryDetailView.as_view(),name='category-detail'),
    path('menu/', views.MenuListCreateView.as_view(),name='menu-list'),
    path('menu/<int:pk>/',views.MenuDetailView.as_view(),name='menu-detail'),
    path('client/categories/<int:pk>/', views.MenuCategoryListRetrive.as_view(),name='client_shop_menu'),
    path('client/menus/<int:pk>/',views.MenuListRetrive.as_view(),name='client_shop_menu'),
] 