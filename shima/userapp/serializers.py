from rest_framework.serializers import ModelSerializer,ValidationError
from rest_framework import serializers

from userapp.models import Users,leave_application,Attendance


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'name',
            'profile_picture',
            'date_of_birth',
            'email',
            'gender',
            'password',
            'guardian_name',
            'guardian_contact_number',
            'number',
            'married',
            'alternate_number',
            'is_form_filled',
            'last_payment',
            "is_superuser",
            'address',
            'pincode',
            'post',
            'aadhar_number',
            'age',
            # "_all_",
        ]
        extra_kwargs = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data) 
        user.set_password(password)
        user.save()
        return user
    
    
    
    
class leave_applicationSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = leave_application
        fields = '__all__'
        
    def create(self, validated_data):
        
        user_id = self.context['request'].user.id # getting user_id from the token
        application = leave_application(**validated_data)
        user_instance = Users.objects.get(id=user_id)
        application.user = user_instance
        application.save()

        return application
    
    
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__' 
    

class NotificationSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
