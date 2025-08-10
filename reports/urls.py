from django.urls import include, path
from . import views


urlpatterns = [
    path('users/',views.UserReportViews.as_view(), name='user_reports'),
    path('organizations/',views.OrganizationReportViews.as_view(),name='organization_report'),
    path('shops/', views.ShopReportViews.as_view(), name='menu_report'),
    path('menus/', views.MenuReportViews.as_view(), name="menu_report"),
    path('orders/',views.OrderReportViews.as_view(),name ='order_report'),
    path('orders/<int:pk>/',views.OrderDetailReportViews.as_view(),name='order_detail_report'),
  
]