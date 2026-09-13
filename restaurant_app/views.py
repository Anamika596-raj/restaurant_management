from django.shortcuts import render, redirect
from .models import MenuItem, Order


def home(request):
    menu_items = MenuItem.objects.filter(available=True)
    message = ''

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        item_id = request.POST.get('item')
        quantity = int(request.POST.get('quantity'))

        item = MenuItem.objects.get(id=item_id)

        Order.objects.create(
            customer_name=customer_name,
            item=item,
            quantity=quantity
        )

        message = f'Order placed successfully! Thank you, {customer_name}.'

    return render(request, 'restaurant_app/home.html', {
        'menu_items': menu_items,
        'message': message
    })


def my_orders(request):
    customer_name = request.GET.get('customer_name', '')
    orders = []

    if customer_name:
        orders = Order.objects.filter(
            customer_name__iexact=customer_name
        ).select_related('item')

    return render(request, 'restaurant_app/orders.html', {
        'orders': orders,
        'customer_name': customer_name
    })


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()

    return redirect('my_orders')


def edit_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.quantity = int(request.POST.get('quantity'))
        order.save()

        return redirect(
            f'/orders/?customer_name={order.customer_name}'
        )

    return render(request, 'restaurant_app/edit_order.html', {
        'order': order
    })


def dashboard(request):
    total_orders = Order.objects.count()
    total_menu_items = MenuItem.objects.count()

    pending_orders = Order.objects.filter(status='Pending').count()
    preparing_orders = Order.objects.filter(status='Preparing').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()

    total_sales = 0

    for order in Order.objects.all():
        total_sales += order.item.price * order.quantity

    recent_orders = Order.objects.all().select_related('item').order_by('-order_date')[:10]

    return render(request, 'restaurant_app/dashboard.html', {
        'total_orders': total_orders,
        'total_menu_items': total_menu_items,
        'pending_orders': pending_orders,
        'preparing_orders': preparing_orders,
        'delivered_orders': delivered_orders,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
    })