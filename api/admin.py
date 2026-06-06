from django.contrib import admin

from django.contrib import admin

from .models import (
    Platform,
    Subscription,
    PaymentMethod,
    Payment,
    ExpenseReport,
)


admin.site.register(Platform)
admin.site.register(Subscription)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(ExpenseReport)
