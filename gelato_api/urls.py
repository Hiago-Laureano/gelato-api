from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, CategoryViewSet, ComplementViewSet, OrderViewSet, UserViewSet

router = routers.SimpleRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("complements", ComplementViewSet)
router.register("orders", OrderViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]