from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from api.models import Subscription, Platform, Payment, PaymentMethod



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "password": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        return user


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["id", "name"]


class SubscriptionSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer(read_only=True)
    platform_id = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(),
        source="platform",
        write_only=True
    )

    class Meta:
        model = Subscription
        fields = [
            "id",
            "cost",
            "name",
            "start_date",
            "status",
            "end_date",
            "platform",
            "platform_id"
        ]
    def validate(self, data):
        start_date = data.get("start_date", getattr(self.instance, "start_date", None))

        end_date = data.get("end_date", getattr(self.instance, "end_date", None))

        if (
            start_date is not None
            and end_date is not None
            and end_date <= start_date
        ):
            raise serializers.ValidationError({
                "end_date": "End date must be later than start date"
            })
        
        allowed_status = ["active", "cancelled", "expired"]

        if data["status"] not in allowed_status:
            raise serializers.ValidationError(
                "Invalid status"
            )
        return data




class PaymentSerializer(serializers.ModelSerializer):
    end_date = serializers.DateField(write_only=True)
    payment_method_name = serializers.CharField(
        source="payment_method.name",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "date",
            "subscription",
            "payment_method",
            "end_date",
            "payment_method_name"
        ]

    def validate(self, data):
        subscription = data["subscription"]
        end_date = data["end_date"]

        if end_date <= subscription.end_date:
            raise serializers.ValidationError({
                "end_date": ("New end date must be later than current subscription end date.")
            })

        return data


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "name",
            "details",
        ]


class AdminUserSerializer(serializers.ModelSerializer):
    subscriptions_count = serializers.IntegerField(read_only=True)
    payments_count = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "subscriptions_count",
            "payments_count",
            "total_spent",
        ]


class MeSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "role",
        ]

    def get_role(self, user):
        if user.is_superuser:
            return "superadmin"

        if user.is_staff:
            return "admin"

        return "user"