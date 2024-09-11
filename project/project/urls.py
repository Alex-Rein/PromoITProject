from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from consultations.views import ListView, SpecialistScheduleView, TestView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('specialists/', ListView.as_view(), name='specialists_list'),
    path('specialists/<int:pk>', SpecialistScheduleView.as_view()),
    # path('schedules/<int:pk>', )


    path('test/', TestView.as_view(), name='test')
]
