def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            count = request.user.cart.items.count()
        except Exception:
            count = 0
    return {"cart_count": count}
