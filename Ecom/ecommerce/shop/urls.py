from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import admin_dashboard, add_category, edit_category, delete_category, add_product, edit_product, delete_product, index, category_products, add_to_cart, view_cart, remove_from_cart

urlpatterns = [
    # Admin URLs
    path('custom-admin/', admin_dashboard, name='admin_dashboard'),
    path('custom-admin/category/add/', add_category, name='add_category'),
    path('custom-admin/category/edit/<int:pk>/', edit_category, name='edit_category'),
    path('custom-admin/category/delete/<int:pk>/', delete_category, name='delete_category'),

    path('custom-admin/product/add/', add_product, name='add_product'),
    path('custom-admin/product/edit/<int:pk>/', edit_product, name='edit_product'),
    path('custom-admin/product/delete/<int:pk>/', delete_product, name='delete_product'),

    # User URLs
    path('', index, name='index'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)