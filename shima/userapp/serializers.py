from rest_framework.serializers import ModelSerializer,ValidationError
from rest_framework import serializers

from userapp.models import Users,leave_application,Attendance,Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields =[
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
        users= validated_data.pop('users', None)
        user_id = self.context['request'].user.id # getting user_id from the token
        if users:
            user_instance=Users.objects.get(id=users)
        else:
            user_instance = Users.objects.get(id=user_id)  
        application = leave_application(**validated_data)
        application.user = user_instance
        application.save()

        return application
    
    
class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__' 
    


class PaymentSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Payment
        fields = '__all__'
    def create(self, validated_data):
        validated_data["user"]=self.context['request'].user
        payment=Payment(**validated_data)
        return payment
