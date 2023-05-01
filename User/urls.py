
from django.urls import path
from .views import (
    UserCreateView,
    UserLoginView
)

# from drf_yasg.views import get_schema_view 
# from drf_yasg import openapi

# #swagger schema
# schema_view = get_schema_view(
#     openapi.Info(
#         title='WorkDistro API',
#         default_version='v1',
#         description='Work Distro API',
#         terms_of_service='null',
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
   
# )


app_name = "Users"

urlpatterns = [
    # path('',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-view'),
    path('register/', UserCreateView.as_view(), name = "account_creation"),
    path('login/', UserLoginView.as_view(), name = "login"),

]