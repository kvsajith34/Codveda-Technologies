from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import ProductForm, CheckoutForm
from .decorators import admin_required


# ── Product listing & detail ──────────────────────────────────────────────────

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    query = request.GET.get("q", "")
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "store/product_list.html", {"products": products, "query": query})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})


# ── Cart ─────────────────────────────────────────────────────────────────────

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "store/cart.html", {"cart": cart})


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    if not product.in_stock:
        messages.warning(request, f"'{product.name}' is out of stock.")
        return redirect("store:product_detail", slug=slug)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if item.quantity < product.stock:
            item.quantity += 1
            item.save()
        else:
            messages.warning(request, "No more stock available.")
    else:
        messages.success(request, f"'{product.name}' added to cart.")
    return redirect("store:cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("store:cart")


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    qty = int(request.POST.get("quantity", 1))
    if qty < 1:
        item.delete()
    else:
        item.quantity = min(qty, item.product.stock)
        item.save()
    return redirect("store:cart")


# ── Checkout & Orders ─────────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("store:cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total=cart.get_total(),
                shipping_address=form.cleaned_data["shipping_address"],
            )
            for ci in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=ci.product,
                    product_name=ci.product.name,
                    quantity=ci.quantity,
                    price=ci.product.price,
                )
                # Deduct stock
                ci.product.stock -= ci.quantity
                ci.product.save()
            cart.items.all().delete()
            messages.success(request, "Order placed successfully!")
            return redirect("store:order_success", pk=order.pk)
    else:
        initial = {"shipping_address": request.user.address}
        form = CheckoutForm(initial=initial)

    return render(request, "store/checkout.html", {"cart": cart, "form": form})


@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "store/order_success.html", {"order": order})


@login_required
def order_list(request):
    orders = request.user.orders.all().order_by("-created_at")
    return render(request, "store/orders.html", {"orders": orders})


# ── Admin dashboard ───────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    products = Product.objects.all().order_by("-created_at")
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "store/admin_dashboard.html", {"products": products, "orders": orders})


@admin_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Product created.")
        return redirect("store:admin_dashboard")
    return render(request, "store/product_form.html", {"form": form, "title": "Add Product"})


@admin_required
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, "Product updated.")
        return redirect("store:admin_dashboard")
    return render(request, "store/product_form.html", {"form": form, "title": "Edit Product"})


@admin_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("store:admin_dashboard")
    return render(request, "store/product_confirm_delete.html", {"product": product})


@admin_required
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f"Order #{pk} status updated.")
    return redirect("store:admin_dashboard")
