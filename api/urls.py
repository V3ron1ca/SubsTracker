from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api import views


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("subscriptions/", views.MySubscriptionsView.as_view(), name="my_subscriptions"),
    path("subscriptions/<int:pk>/", views.SubscriptionDetailView.as_view()),
    path("subscriptions/<int:pk>/payments/create/", views.PaymentCreateView.as_view()),
    path("platforms/", views.PlatformListView.as_view()),
    path(
        "subscriptions/<int:subscription_id>/payments/",
        views.SubscriptionPaymentsView.as_view()
    ),
    path("payment-methods/", views.PaymentMethodListView.as_view()),
    path(
    "payments/<int:pk>/delete/",
    views.PaymentDeleteView.as_view()
),
    path("subscriptions/<int:pk>/delete/", views.SubscriptionDeleteView.as_view()),
    path("statistics/", views.UserStatisticsView.as_view(), name="user_statistics"),
    path("user-platforms/", views.UserPlatformsView.as_view()),
    path("notifications/", views.NotificationsView.as_view()),
    path("admin/users/", views.AdminUsersView.as_view()),
    path("me/", views.MeView.as_view()),
]
