from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from app.models import Product, Order

def statistics_view(request):
    quantity_count = Product.objects.aggregate(quantity_count=Count('quantity'))['quantity_count']

    product_sum = Product.objects.aggregate(total_price=Sum('price'))['total_price']

    sum_price = product_sum

    one_day_ago = timezone.now() - timedelta(days=1)
    orders_last_day = Order.objects.filter(created_at__gte=one_day_ago)

    ten_days_ago = timezone.now() - timedelta(days=10)
    orders_last_10_days = Order.objects.filter(created_at__gte=ten_days_ago)

    orders_last_day_stats = orders_last_day.aggregate(
        total_quantity=Sum('quantity'),
        total_price=Sum('product__price')
    )

    orders_last_10_days_stats = orders_last_10_days.aggregate(
        total_quantity=Sum('quantity'),
        total_price=Sum('product__price')
    )

    context = {
        'quantity_count': quantity_count,
        'product_sum': product_sum,
        'sum_price': sum_price,
        'orders_last_day': orders_last_day,
        'orders_last_day_stats': orders_last_day_stats,
        'orders_last_10_days': orders_last_10_days,
        'orders_last_10_days_stats': orders_last_10_days_stats,
    }

    return render(request, 'statistics.html', context)
