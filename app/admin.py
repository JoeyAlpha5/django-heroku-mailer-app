from django.contrib import admin
from .models import payment
# Register your models here.

class paymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'date']
    ordering = ['date']


admin.site.register(payment, paymentAdmin)

