from rest_framework import routers
from . import views


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'user', views.UserViewSet)
router.register(r'role', views.RoleViewSet)
router.register(r'key', views.KeyViewSet)
urlpatterns = router.urls
