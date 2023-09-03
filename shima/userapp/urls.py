from django.urls import path,include
from rest_framework.routers import DefaultRouter
from userapp.views import UserViewSet ,RegistrationView,LoginView, LeaveApplicationViewSet,RefreshTokenView,AttendanceViewSet,GetUserLeaveApplications,AttendanceFilterView,PaymentViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet),
router.register(r'leave-applications',  LeaveApplicationViewSet),
router.register(r'attendance', AttendanceViewSet)
router.register(r'payment', PaymentViewSet)


urlpatterns = [
  
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('get_leave_applications/', GetUserLeaveApplications.as_view()  ),
    path('token/', RefreshTokenView.as_view()),
    path('attendance/filter/', AttendanceFilterView.as_view()),
    path('', include(router.urls)),
   
]