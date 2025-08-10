from django.urls import include, path
from orders import views


urlpatterns = [
    path('', views.OrderListCreateView.as_view(),name='order_list_create'),
    path('<int:pk>/', views.OrderDetailView.as_view(),name='order_details'),
    path('order-items/', views.OrderItemListCreate.as_view(),name='order_items_list_create'),
    path('order-items/<int:pk>', views.OrderItemDetail.as_view(),name='order_items_details'),
    path('menu-rates/', views.MenuRateListCreateView.as_view(),name='menu_rate_list_create'),
    path('menu-rates/<int:pk>', views.MenuRateDetailView.as_view(), name='menu_rate_detail'),
    path('kitchen-display/',views.KitchenDisplayListView.as_view(),name='kitchen_display_list'),
   
]