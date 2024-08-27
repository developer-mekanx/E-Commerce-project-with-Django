from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_panel_add/', views.admin_panel_add, name='admin_panel_add'),
    path('admin_panel_list/', views.admin_panel_list, name='admin_panel_list'),
    path('admin_panel_edit/<int:pk>/', views.admin_panel_edit, name='admin_panel_edit'),
    path('admin_panel_delete/<int:pk>/', views.admin_panel_delete, name='admin_panel_delete'),
    path('admin_panel_search/', views.admin_panel_search, name='admin_panel_search'),
    path('admin_panel_search2/', views.admin_panel_search2, name='admin_panel_search2'),
]