from django.urls import path
from .import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('registor/',views.Registor_User_View),
    path('login/',views.Login_View),
    path('mark_spam/',views.Mark_Spam_View),
    path('phoneno_search/',views.Phone_No_Search_View),
    path('name_search/',views.Name_Search_View),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify_token/', TokenVerifyView.as_view(), name='token_Verify'),
]