from django.urls import path
from mysss import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('my-cart/', views.my_cart_view, name='my_cart'),
    path('shop/', views.shop, name='shop'),
    path('purchases/', views.purchases_view, name='purchases'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('shop/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product-details/<int:product_id>/', views.product_details, name='product_details'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
