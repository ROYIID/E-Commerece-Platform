from django.db import models


class Product(models.Model):
    # ─── Existing DB columns ─────────────────────────────
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.TextField(null=True, blank=True)  # original DB price field
    main_category = models.TextField(null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    item_id = models.TextField(primary_key=True)  # NOT NULL in DB

    # ─── Your new fields (not in database yet!) ──────────
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_decimal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "meta"  # <-- your real table name
        managed = False    # <-- don't let Django create or alter the table

class UserAction(models.Model):
    LIKE = "like"
    CART = "cart"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)