import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'virginpreps.settings')
django.setup()

from oscar.apps.catalogue.models import ProductClass, AttributeOptionGroup, AttributeOption

# Get or create the Vegetable product class
vegetable_class, created = ProductClass.objects.get_or_create(
    name="vegetable",
    slug="vegetable"
)

# Create the option group
option_group, created = AttributeOptionGroup.objects.get_or_create(
    name="Produce Type"
)

# Add options to the group
AttributeOption.objects.get_or_create(
    group=option_group,
    option="general"
)
AttributeOption.objects.get_or_create(
    group=option_group,
    option="organic"
)

# Create the product attribute
vegetable_class.attributes.get_or_create(
    name="Produce Type",
    code="produce_type",
    type="option",
    option_group=option_group,
    required=True
)