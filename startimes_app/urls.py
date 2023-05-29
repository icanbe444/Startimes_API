from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


urlpatterns = [ 
    
    path('startimes_api/payment/validate', views.ValidationView.as_view(), name='validate'),
    # path('startimes_api/payment', views.PaymentView.as_view(), name='confirmpayment'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

]