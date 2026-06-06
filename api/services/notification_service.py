from api.models import Subscription
from django.db.models import F, ExpressionWrapper, DurationField
from datetime import timedelta
from django.utils import timezone
from datetime import date
from typing import TypedDict


class NotificationDict(TypedDict):
    id: int
    name: str
    end_date: date
    days_left: int
    message: str


class NotificationService:
    @staticmethod
    def get_user_notifications(user) -> list[NotificationDict]:
        today = timezone.now().date()
        subscriptions = (
            Subscription.objects
            .filter(
                user=user,
                status="active",
                end_date__range=(today, today + timedelta(days=7))
            )
            .annotate(
                days_left=ExpressionWrapper(
                    F("end_date") - today,
                    output_field=DurationField()
                )
            )
        )

        notifications = [
            {
                "id": sub.id,
                "name": sub.name,
                "end_date": sub.end_date,
                "days_left": (sub.end_date - today).days,
                "message": f"Subskrypcja {sub.name} kończy się za {(sub.end_date - today).days} dni"
            }
            for sub in subscriptions
        ]
        return notifications
