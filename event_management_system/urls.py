from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from users.views import UserCreateView, CustomAuthToken
from events.views import EventViewSet
from rspvs.views import RSVPViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'rsvps', RSVPViewSet)

schema_view = get_schema_view(
    openapi.Info(title="Event API", default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/token/', CustomAuthToken.as_view(), name='api-token'),  # Using custom token view
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
