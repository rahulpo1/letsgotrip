from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    path('book/<int:pk>/', views.book_package, name='book_package'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),

    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/packages/', views.vendor_packages, name='vendor_packages'),
    path('vendor/add-package/', views.add_package, name='add_package'),
    path('vendor/bookings/', views.vendor_bookings, name='vendor_bookings'),
    path('vendor/packages/edit/<int:pk>/', views.edit_package, name='edit_package'),
    path('vendor/packages/delete/<int:pk>/', views.delete_package, name='delete_package'),

]

