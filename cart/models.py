from django.db import models
from store.models import Product
from accounts.models import CustomUser

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, unique=True, blank=True, null=True)  # Allow null for database consistency
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id or "Anonymous Cart"

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # Prevent deletion issues
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Ensure non-negative quantities
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"
