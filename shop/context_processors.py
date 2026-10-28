def cart_processor(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {'cart_item_count': total_items, 'cart_dict': cart}
