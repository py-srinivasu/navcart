from rest_framework import routers

from apps.cart.views import CartViewSet


router = routers.DefaultRouter()
router.register('cart', CartViewSet, 'cart')


urlpatterns = router.urls
