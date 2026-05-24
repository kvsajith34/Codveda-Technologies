from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # Cart
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update_cart"),

    # Checkout & Orders
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:pk>/success/", views.order_success, name="order_success"),

    # Admin
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/product/new/", views.product_create, name="product_create"),
    path("dashboard/product/<slug:slug>/edit/", views.product_edit, name="product_edit"),
    path("dashboard/product/<slug:slug>/delete/", views.product_delete, name="product_delete"),
    path("dashboard/order/<int:pk>/status/", views.order_update_status, name="order_update_status"),
]
