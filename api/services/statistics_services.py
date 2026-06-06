from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from api.models import Subscription


class StatisticsService:

    @staticmethod
    def get_user_statistics(user, platform_name=None):

        subscriptions = Subscription.objects.filter(user=user)

        if platform_name:
            subscriptions = subscriptions.filter(platform__name=platform_name)

        total_spent = subscriptions.aggregate(
            total=Sum("cost")
        )["total"] or 0

        active_subscriptions = subscriptions.filter(
            status="active"
        ).count()

        monthly_spending = subscriptions.annotate(
            month=TruncMonth("start_date")
        ).values(
            "month"
        ).annotate(
            total=Sum("cost")
        ).order_by("month")

        spending_by_platform = subscriptions.values(
            "platform__name"
        ).annotate(
            total_spent=Sum("cost"),
            subscriptions_count=Count("id")
        ).order_by("-total_spent")

        most_expensive = subscriptions.order_by("-cost").first()

        return {
            "total_spent": total_spent,
            "active_subscriptions": active_subscriptions,

            "most_expensive_platform": {
                "platform": most_expensive.platform.name if most_expensive else None,
                "cost": most_expensive.cost if most_expensive else 0
            } if most_expensive else None,

            "spending_by_platform": list(spending_by_platform),
            "monthly_spending": list(monthly_spending),
        }