from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import GroupViewset, HoneyViewset, StockViewset, OrderViewset, FeedbackViewset
from .auth_views import login_view, logout_view, user_view

router = DefaultRouter()
router.register("groups", GroupViewset, basename="groups")
router.register("honey", HoneyViewset, basename="honey")
router.register("stock", StockViewset, basename="stock")
router.register("orders", OrderViewset, basename="orders")
router.register("feedback", FeedbackViewset, basename="feedback")

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', user_view, name='user'),
]