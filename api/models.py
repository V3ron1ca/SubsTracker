from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import F, Q


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SubscriptionStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    CANCELLED = "cancelled", "Cancelled"
    EXPIRED = "expired", "Expired"  

class Subscription(models.Model):
    name = models.CharField(max_length=100)

    start_date = models.DateField()
    end_date = models.DateField()

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    class Meta:
        constraints = [models.CheckConstraint(condition=Q(end_date__gt=F("start_date")),
                                              name="subscription_end_after_start")]
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError({
                "end_date": "End date must be later than start date"
            })
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return (
            f"{self.name}"
            f"{self.user.username}"
        )
    


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.name


class Payment(models.Model):
    end_date = models.DateField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    date = models.DateField()

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    def __str__(self):
        return (
            f"{self.subscription.name}"
            f"{self.amount} ZŁ ({self.date})"
            )
    

class ExpenseReport(models.Model):
    date_from = models.DateField()

    date_to = models.DateField()

    category = models.CharField(max_length=100)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    administrator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expense_reports"
    )

    class Meta:
            constraints = [models.CheckConstraint(condition=Q(date_to__gte=F("date_from")),
                                                  name="report_end_after_start"
            )
        ]

    def clean(self):
        if self.date_to < self.date_from:
            raise ValidationError({
                "date_to": "End date cannot be earlier than start date"
            })
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.category} "
            f"({self.date_from} - {self.date_to})"
        )