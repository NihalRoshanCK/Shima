from rest_framework.views import APIView
from datetime import date
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView

from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from userapp.models import Users,leave_application,Attendance,Payment
from django.contrib.auth import authenticate
from userapp.serializers import UserSerializer,leave_applicationSerializer,AttendanceSerializer,PaymentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from userapp.utilities import genarate_otp
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime




class RefreshTokenView(TokenRefreshView):
    pass


class RegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save the user instance

        # Generate OTP
        otp=genarate_otp(user)
        # Generate token
        refresh = RefreshToken.for_user(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'otp': otp
        }
        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            try:
                user=Users.objects.get(email=email)
            except Users.DoesNotExist:
                return Response({"detail": "No active account found with the given credentials"}, status=401)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                data={
                    'message': 'LOGIND',
                    'user': UserSerializer(user).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
                return Response(data, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    



class LeaveApplicationViewSet(viewsets.ModelViewSet):
    queryset = leave_application.objects.all()
    serializer_class = leave_applicationSerializer



    def get_permissions(self):
        if self.action in ['partial_update', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [AllowAny()]
        else:
            return [IsAdminUser()]
    
        def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()

            # Check if the current user is the owner of the instance or an admin
            if instance == request.user or request.user.is_superuser:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise ValidationError("You are not allowed to retrieve this user's data.")
    
        def partial_update(self, request, *args, **kwargs):
            instance = self.get_object()

            # Check if the current user is the owner of the instance or an admin
            if instance == request.user or request.user.is_superuser:
                return super().partial_update(request, *args, **kwargs)
            else:
                raise ValidationError("You are not allowed to update this user's data.")
    
        
class GetUserLeaveApplications(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = leave_applicationSerializer

    def get_queryset(self):
        user = self.request.user
        return leave_application.objects.filter(user=user)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    # permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action in ['partial_update', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [AllowAny()]
        else:
            return [IsAdminUser()]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the current user is the owner of the instance or an admin
        if instance == request.user or request.user.is_superuser:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            raise ValidationError("You are not allowed to retrieve this user's data.")
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the current user is the owner of the instance or an admin
        if instance == request.user or request.user.is_superuser:
            return super().partial_update(request, *args, **kwargs)
        else:
            raise ValidationError("You are not allowed to update this user's data.")
    
class UsersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_authenticated_user(self, request):
        authentication = JWTAuthentication()
        user, _ = authentication.authenticate(request)
        return user

    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = self.get_authenticated_user(request)
        if user:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'])
    def mark_attendance_bulk(self, request):
        attendance_data = request.data.get('attendance_data', [])
        success_count = 0
        failed_count = 0
        for entry in attendance_data:
            user_id = entry.get('user_id')
            attendance_date = entry.get('attendance_date')
            is_present = entry.get('is_present', False)
            try:
                user = Users.objects.get(pk=user_id)
                Attendance.objects.create(user=user, date=attendance_date, is_present=is_present)
                success_count += 1
            except Users.DoesNotExist:
                failed_count += 1
        return Response({
            'message': f'Successfully marked attendance for {success_count} users',
            'failed_count': failed_count
        }, status=status.HTTP_200_OK)
    

class AttendanceFilterView(ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        user_id=None
        start_date = self.request.query_params.get('start_date',None)
        end_date = self.request.query_params.get('end_date',None)
        if user.is_superuser:
            user_id = self.request.query_params.get('user',None)

        queryset = Attendance.objects.all()

        if start_date and end_date:
            
            queryset = queryset.filter(date__range=[start_date, end_date])
            
        if user.is_superuser  and user_id:
            
            queryset = queryset.filter(user_id=user_id)
        
        elif not user.is_superuser :
        
            queryset = queryset.filter(user=user)
        
        return queryset

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'user_payments':
            return [IsAuthenticated()]
        elif self.action == 'pending_payments':
            return [IsAdminUser()]
        else:
            return [IsAdminUser()]

    @action(detail=False, methods=['GET'])
    def user_payments(self, request, user_reference=None):
        # Get payments for a specific user or for the requesting user
        user = self.request.user
        if user.is_superuser:
            payments=Payment.objects.all()
        else:
            payments = Payment.objects.filter(user=user)
        # if user_reference:
        #     user = Users.objects.get(reference=user_reference)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def pending_payments(self, request):
        # Get a list of users with pending payments
        pending_users = Users.objects.filter(
            ~Q(payment__payment_date__month=now().month)
        )

        serializer = UsersSerializer(pending_users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def calculate_revenue(self, request):
        start_date = request.query_params.get('start_date',None)
        end_date = request.query_params.get('end_date',None)
        start_year = request.query_params.get('start_year',None)
        end_year = request.query_params.get('end_year',None)
        queryset=Payment.objects.all()
        # Calculate revenue and difference based on query parameters
        if start_year and end_year:
            queryset = queryset.filter(payment_date__year__range=[start_year, end_year])
        elif start_year:
            queryset = queryset.filter(payment_date__year=start_year)
        elif start_date and end_date:
            queryset = queryset.filter(payment_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(payment_date__month=start_date.month, payment_date__year=start_date.year)
        else:
            today = datetime.today()
            queryset = queryset.filter(payment_date__month=today.month, payment_date__year=today.year)
        
        

        total_revenue = queryset.aggregate(total=Sum('amount'))['total'] or 0

    

        return Response({'total_revenue': total_revenue}, status=status.HTTP_200_OK)