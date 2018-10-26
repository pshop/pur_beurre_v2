from django.urls import path
from products import views

urlpatterns = [
    path('', views.search_products, name='search'),
    path('result/<data>', views.display_results, name='display_results'),
    path('product/<product_id>', views.product_info, name='product_info'),
    path('save/<product_id>', views.save_product, name='save_product'),
    path('delete/<product_id>', views.delete_product, name='delete_product'),
    path('favorites/<user_name>', views.display_favorites, name='display_favorites'),
    path('legals/', views.legals, name='legals'),
]