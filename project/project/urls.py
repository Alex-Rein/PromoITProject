from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from consultations.views import (SpecialistsListView, SpecialistDetailView, TestView,
                                 AdminUserListView, AdminUserActionView,
                                 SlotCreateView,
                                 AppointmentCreateView, AppointmentCancelView,
                                 SpecialistScheduleCreateView, SpecialistScheduleView, SpecialistRegisterView)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Authentication endpoints
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # Administration endpoints
    path('users/', AdminUserListView.as_view(), name='admin_user_list'),
    path('users/<int:pk>', AdminUserActionView.as_view(), name='admin_user_action'),

    # User endpoints
    path('specialists/', SpecialistsListView.as_view(), name='specialists_list'),
    path('specialists/<int:pk>', SpecialistDetailView.as_view(), name='specialist_details'),
    path('appointment/<int:pk>', AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('slots/<int:pk>/signup', AppointmentCreateView.as_view(), name='appointment_signup'),

    # Specialist endpoints
    path('specialist/register', SpecialistRegisterView.as_view(), name='specialist_register'),
    path('specialist/my_schedule', SpecialistScheduleView.as_view(), name='specialist_schedule'),
    path('specialist/add_schedule', SpecialistScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/<int:pk>', SlotCreateView.as_view(), name='slot_create'),
]




