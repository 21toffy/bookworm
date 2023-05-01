from django.contrib import admin
from django.urls import path, include


from drf_yasg.views import get_schema_view 
from drf_yasg import openapi

#swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title='BookWorm API',
        default_version='v1',
        description='BookWorm API',
        terms_of_service='null',
        license=openapi.License(name="BSD License"),
    ),
    public=True,
   
)



urlpatterns = [
    path('',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-view'),
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('User.urls')),
    path('api/v1/book/', include('Book.urls'))
]
