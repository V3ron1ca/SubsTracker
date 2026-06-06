from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from api.serializers import RegisterSerializer, SubscriptionSerializer,\
      PlatformSerializer, PaymentSerializer, PaymentMethodSerializer, \
      AdminUserSerializer, MeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from api.models import Subscription, Payment, PaymentMethod, Platform
from rest_framework.response import Response
from api.services.statistics_services import StatisticsService
from api.services.notification_service import NotificationService
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from decimal import Decimal


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MySubscriptionsView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Subscription.objects
               .filter(user=self.request.user)
               .select_related("platform")
               .order_by("-start_date")
    
        )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class SubscriptionDeleteView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
class PlatformListView(generics.ListAPIView):
    queryset = Platform.objects.all() ##order_by("name")??
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        subscription = serializer.validated_data["subscription"]

        if subscription.user != self.request.user:
            raise PermissionDenied(
                "You cannot add payment to other subscription"
            )
        
        serializer.save()

class PaymentDeleteView(generics.DestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            subscription__user=self.request.user
        )


class SubscriptionPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subscription_id = self.kwargs["subscription_id"]

        return (
            Payment.objects
            .filter(subscription_id=subscription_id, subscription__user=self.request.user,)
            .select_related("subscription", "payment_method",)
            .order_by("-date")
        )


class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]


class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response( StatisticsService.get_user_statistics(
            user=request.user,
            platform_name=request.query_params.get("platform")
        ))
    

class UserPlatformsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        platforms = Subscription.objects.filter(
            user=request.user
        ).values_list(
            "platform__name",
            flat=True
        ).distinct()

        return Response(list(platforms))


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = NotificationService.get_user_notifications(request.user)
        return Response({
            "count": len(notifications),
            "results": notifications
        })


class AdminUsersView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.annotate(
            subscriptions_count=Count(
                "subscriptions",
                distinct=True
            ),
            payments_count=Count(
                "subscriptions__payments",
                distinct=True
            ),
            total_spent=Coalesce(
                Sum("subscriptions__payments__amount"),
                Decimal("0.00")
            )
        ).order_by("-date_joined")


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
