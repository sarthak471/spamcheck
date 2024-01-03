from rest_framework import serializers
class Validate_User_Data(serializers.Serializer):
    Name = serializers.CharField(max_length=100)
    Password = serializers.CharField(max_length=100)
    Phone_no = serializers.IntegerField()
    Email = serializers.CharField(max_length=100,allow_blank=True, default=None)

class Validate_Login_Data(serializers.Serializer):
    Phone_no = serializers.IntegerField()
    Password = serializers.CharField()

class Validate_Phone_no(serializers.Serializer):
    Phone_no = serializers.IntegerField()

class Validate_Name(serializers.Serializer):
    Name = serializers.CharField(max_length=100)