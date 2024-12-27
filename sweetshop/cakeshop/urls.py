from django.urls import include, path, re_path
from cakeshop import views
from django.conf import settings
from django.conf.urls.static import static
from .views import register, UserLoginView, UserLogoutView
from rest_framework.routers import DefaultRouter
from .views_api import CakeViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"cakes", CakeViewSet, basename="cake")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    # Десерты
    re_path(r"^cakes/$", views.CakeListView.as_view(), name="cakes"),
    re_path(r"^cake/(?P<pk>\d+)$", views.CakeDetailView.as_view(), name="cake-detail"),
    # Отзывы
    path("cake/<int:cake_id>/add_review/", views.add_review, name="add-review"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit-review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete-review"),
    # Аутентификация
    path("register/", register, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    # Корзина
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:cake_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    # Заказы
    path("orders/", views.order_list, name="order_list"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),

    path('api/', include(router.urls)),
]
