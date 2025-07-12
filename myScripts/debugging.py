import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'virginpreps.settings')
django.setup()

# In your homepage view or template context
from oscar.apps.catalogue.models import Product
print(Product.objects.all().count())  # Check total products
print(Product.objects.browsable().count())  # Check browsable products

from oscar.apps.catalogue.models import Category
# print(dir(Category))
category = Category.objects.get(name="Rice")
products = category.product_set.all()
# print(categSory)  # Should match what you expect
print(products, products.count())  # Should match what you expect