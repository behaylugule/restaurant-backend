from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    org_name = serializers.CharField(source='organization.name',read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = User
        fields = ('id','username','first_name','middle_name','last_name','contact_number', 'email','role', 'password','organization','shop','org_name','shop_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False}
        }

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        role = validated_data.pop('role', 'user')
        request = self.context.get('request')
        organization = None
        if request and request.user.is_authenticated:
            if request.user.role != 'admin' and request.user.organization:
                organization = request.user.organization

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            **validated_data
        )

        if organization:
            user.organization = organization
            user.save()
        return user


class PasswardChangeSerializer(serializers.Serializer):
       old_password = serializers.CharField(required=True)
       new_password = serializers.CharField(required=True) 