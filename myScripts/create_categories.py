import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../virginpreps.settings')
django.setup()

from oscar.apps.catalogue.categories import create_from_breadcrumbs

categories = [
    # ===== STAPLES =====
    "Pulses & Lentils",
    "Pulses & Lentils > Whole",
    "Pulses & Lentils > Whole > With Skin",
    "Pulses & Lentils > Whole > Without Skin",
    "Pulses & Lentils > Split",
    "Pulses & Lentils > Split > With Skin",
    "Pulses & Lentils > Split > Without Skin",
    "Pulses & Lentils > Broken",
    "Pulses & Lentils > Flour",
    
    "Rice",
    "Rice > White",
    "Rice > White > Regular",
    "Rice > White > Premium",
    "Rice > Brown",
    "Rice > Red/Black",
    "Rice > Parboiled",
    
    "Wheat & Atta",
    "Wheat & Atta > Whole Wheat",
    "Wheat & Atta > Multigrain",
    "Wheat & Atta > Fortified",
    
    "Millets",
    "Millets > Foxtail",
    "Millets > Barnyard",
    "Millets > Little",
    
    # ===== COOKING ESSENTIALS =====
    "Oils",
    "Oils > Cold-Pressed",
    "Oils > Cold-Pressed > Coconut",
    "Oils > Cold-Pressed > Mustard",
    "Oils > Refined",
    "Oils > Refined > Sunflower",
    "Oils > Refined > Soybean",
    
    "Ghee & Butter",
    "Ghee & Butter > Cow",
    "Ghee & Butter > Buffalo",
    "Ghee & Butter > Flavored",
    
    "Spices",
    "Spices > Whole Spices",
    "Spices > Whole Spices > Cumin",
    "Spices > Whole Spices > Cardamom",
    "Spices > Powdered Spices",
    "Spices > Powdered Spices > Turmeric",
    "Spices > Powdered Spices > Red Chili",
    "Spices > Blended Masalas",
    
    # ===== SWEETENERS =====
    "Sugar & Sweeteners",
    "Sugar & Sweeteners > White Sugar",
    "Sugar & Sweeteners > Brown Sugar",
    "Sugar & Sweeteners > Jaggery",
    "Sugar & Sweeteners > Jaggery > Solid",
    "Sugar & Sweeteners > Jaggery > Powder",
    "Sugar & Sweeteners > Honey",
    
    # ===== DAIRY =====
    "Milk",
    "Milk > Cow Milk",
    "Milk > Buffalo Milk",
    "Milk > Toned",
    "Milk > Full Cream",
    
    "Dairy Products",
    "Dairy Products > Paneer",
    "Dairy Products > Yogurt",
    "Dairy Products > Cheese",
    "Dairy Products > Buttermilk",
    
    # ===== NUTS & DRY FRUITS =====
    "Nuts",
    "Nuts > Almonds",
    "Nuts > Almonds > Whole",
    "Nuts > Almonds > Sliced",
    "Nuts > Cashews",
    "Nuts > Walnuts",
    
    "Dry Fruits",
    "Dry Fruits > Raisins",
    "Dry Fruits > Dates",
    "Dry Fruits > Figs",
    
    # ===== FRESH PRODUCE =====
    "Vegetables",
    "Vegetables > Leafy Greens",
    "Vegetables > Leafy Greens > Spinach",
    "Vegetables > Leafy Greens > Coriander",
    "Vegetables > Root Vegetables",
    "Vegetables > Root Vegetables > Potato",
    "Vegetables > Root Vegetables > Onion",
    "Vegetables > Gourds",
    
    "Fruits",
    "Fruits > Tropical",
    "Fruits > Tropical > Banana",
    "Fruits > Tropical > Mango",
    "Fruits > Citrus",
    "Fruits > Citrus > Orange",
    "Fruits > Citrus > Lemon",
    
    # ===== READY-TO-EAT =====
    "Ready-to-Eat",
    "Ready-to-Eat > Breakfast Cereals",
    "Ready-to-Eat > Instant Mixes",
    "Ready-to-Eat > Instant Mixes > Dosa Mix",
    "Ready-to-Eat > Instant Mixes > Idli Mix",
    "Ready-to-Eat > Snacks",
    "Ready-to-Eat > Snacks > Namkeen",
    "Ready-to-Eat > Snacks > Biscuits",
    
    # ===== BEVERAGES =====
    "Beverages",
    "Beverages > Health Drinks",
    
    # ===== INTERNATIONAL =====
    "International Foods",
    "International Foods > Pasta",
    "International Foods > Pasta > Penne",
    "International Foods > Pasta > Spaghetti",
    "International Foods > Sauces",
    "International Foods > Sauces > Pasta Sauce",
    "International Foods > Sauces > Soy Sauce"
]


for breadcrumbs in categories:
    create_from_breadcrumbs(breadcrumbs)

print("categories created")