"""
Django management command to populate the database with fake data.
Uses online images from Unsplash for product photos.

Usage: uv run python manage.py populate_data
"""

import random
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Category, Product
from coupons.models import Coupon
from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Populate the database with fake categories, products, coupons, and orders'

    # Category data with names in English and Spanish
    CATEGORIES = [
        {
            'en': {'name': 'Electronics', 'slug': 'electronics'},
            'es': {'name': 'Electrónica', 'slug': 'electronica'},
        },
        {
            'en': {'name': 'Clothing', 'slug': 'clothing'},
            'es': {'name': 'Ropa', 'slug': 'ropa'},
        },
        {
            'en': {'name': 'Home & Garden', 'slug': 'home-garden'},
            'es': {'name': 'Hogar y Jardín', 'slug': 'hogar-jardin'},
        },
        {
            'en': {'name': 'Sports & Outdoors', 'slug': 'sports-outdoors'},
            'es': {'name': 'Deportes y Exterior', 'slug': 'deportes-exterior'},
        },
        {
            'en': {'name': 'Books', 'slug': 'books'},
            'es': {'name': 'Libros', 'slug': 'libros'},
        },
        {
            'en': {'name': 'Beauty & Health', 'slug': 'beauty-health'},
            'es': {'name': 'Belleza y Salud', 'slug': 'belleza-salud'},
        },
        {
            'en': {'name': 'Toys & Games', 'slug': 'toys-games'},
            'es': {'name': 'Juguetes y Juegos', 'slug': 'juguetes-juegos'},
        },
        {
            'en': {'name': 'Food & Beverages', 'slug': 'food-beverages'},
            'es': {'name': 'Alimentos y Bebidas', 'slug': 'alimentos-bebidas'},
        },
    ]

    # Product data organized by category
    PRODUCTS = {
        'electronics': [
            {'name': 'Wireless Bluetooth Headphones', 'name_es': 'Auriculares Bluetooth Inalámbricos', 'price': 79.99, 'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'},
            {'name': 'Smart Watch Pro', 'name_es': 'Reloj Inteligente Pro', 'price': 249.99, 'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'},
            {'name': 'Portable Power Bank 20000mAh', 'name_es': 'Batería Portátil 20000mAh', 'price': 45.99, 'image': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500'},
            {'name': 'Wireless Charging Pad', 'name_es': 'Cargador Inalámbrico', 'price': 29.99, 'image': 'https://images.unsplash.com/photo-1586816879360-004f5b0c51e3?w=500'},
            {'name': 'Mechanical Gaming Keyboard', 'name_es': 'Teclado Mecánico Gaming', 'price': 129.99, 'image': 'https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500'},
            {'name': 'Ultra HD Webcam', 'name_es': 'Webcam Ultra HD', 'price': 89.99, 'image': 'https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=500'},
        ],
        'clothing': [
            {'name': 'Premium Cotton T-Shirt', 'name_es': 'Camiseta de Algodón Premium', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500'},
            {'name': 'Classic Denim Jacket', 'name_es': 'Chaqueta de Mezclilla Clásica', 'price': 89.99, 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500'},
            {'name': 'Slim Fit Chinos', 'name_es': 'Pantalones Chinos Slim Fit', 'price': 59.99, 'image': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=500'},
            {'name': 'Wool Blend Sweater', 'name_es': 'Suéter de Mezcla de Lana', 'price': 79.99, 'image': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=500'},
            {'name': 'Running Sneakers', 'name_es': 'Zapatillas para Correr', 'price': 119.99, 'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500'},
            {'name': 'Leather Belt', 'name_es': 'Cinturón de Cuero', 'price': 44.99, 'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500'},
        ],
        'home-garden': [
            {'name': 'Modern LED Table Lamp', 'name_es': 'Lámpara de Mesa LED Moderna', 'price': 54.99, 'image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500'},
            {'name': 'Indoor Plant Pot Set', 'name_es': 'Set de Macetas para Interior', 'price': 39.99, 'image': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=500'},
            {'name': 'Cozy Throw Blanket', 'name_es': 'Manta Acogedora', 'price': 49.99, 'image': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500'},
            {'name': 'Scented Candle Collection', 'name_es': 'Colección de Velas Aromáticas', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1602028915047-37269d1a73f7?w=500'},
            {'name': 'Wall Clock Minimalist', 'name_es': 'Reloj de Pared Minimalista', 'price': 29.99, 'image': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=500'},
            {'name': 'Kitchen Knife Set', 'name_es': 'Set de Cuchillos de Cocina', 'price': 89.99, 'image': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=500'},
        ],
        'sports-outdoors': [
            {'name': 'Yoga Mat Premium', 'name_es': 'Esterilla de Yoga Premium', 'price': 49.99, 'image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500'},
            {'name': 'Resistance Bands Set', 'name_es': 'Set de Bandas de Resistencia', 'price': 24.99, 'image': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500'},
            {'name': 'Insulated Water Bottle', 'name_es': 'Botella de Agua Térmica', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500'},
            {'name': 'Hiking Backpack 40L', 'name_es': 'Mochila de Senderismo 40L', 'price': 79.99, 'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500'},
            {'name': 'Fitness Tracker Band', 'name_es': 'Pulsera de Actividad Física', 'price': 59.99, 'image': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500'},
            {'name': 'Camping Tent 4-Person', 'name_es': 'Tienda de Campaña 4 Personas', 'price': 149.99, 'image': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=500'},
        ],
        'books': [
            {'name': 'The Art of Programming', 'name_es': 'El Arte de la Programación', 'price': 39.99, 'image': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500'},
            {'name': 'Modern Photography Guide', 'name_es': 'Guía de Fotografía Moderna', 'price': 44.99, 'image': 'https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=500'},
            {'name': 'Healthy Cooking Recipes', 'name_es': 'Recetas de Cocina Saludable', 'price': 29.99, 'image': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=500'},
            {'name': 'Business Success Strategies', 'name_es': 'Estrategias de Éxito Empresarial', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500'},
            {'name': 'Mindfulness & Meditation', 'name_es': 'Mindfulness y Meditación', 'price': 24.99, 'image': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=500'},
            {'name': 'World History Encyclopedia', 'name_es': 'Enciclopedia de Historia Mundial', 'price': 59.99, 'image': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500'},
        ],
        'beauty-health': [
            {'name': 'Vitamin C Serum', 'name_es': 'Sérum de Vitamina C', 'price': 29.99, 'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500'},
            {'name': 'Natural Face Moisturizer', 'name_es': 'Crema Hidratante Facial Natural', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500'},
            {'name': 'Essential Oils Set', 'name_es': 'Set de Aceites Esenciales', 'price': 44.99, 'image': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=500'},
            {'name': 'Hair Care Bundle', 'name_es': 'Kit de Cuidado del Cabello', 'price': 49.99, 'image': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=500'},
            {'name': 'Bamboo Toothbrush Set', 'name_es': 'Set de Cepillos de Bambú', 'price': 14.99, 'image': 'https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=500'},
            {'name': 'Digital Body Scale', 'name_es': 'Báscula Digital Corporal', 'price': 39.99, 'image': 'https://images.unsplash.com/photo-1576678927484-cc907957088c?w=500'},
        ],
        'toys-games': [
            {'name': 'Building Blocks 500pcs', 'name_es': 'Bloques de Construcción 500pzs', 'price': 49.99, 'image': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500'},
            {'name': 'Remote Control Car', 'name_es': 'Coche de Control Remoto', 'price': 69.99, 'image': 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=500'},
            {'name': 'Classic Board Game Set', 'name_es': 'Set de Juegos de Mesa Clásicos', 'price': 39.99, 'image': 'https://images.unsplash.com/photo-1632501641765-e568d28b0015?w=500'},
            {'name': 'Puzzle 1000 Pieces', 'name_es': 'Puzzle 1000 Piezas', 'price': 24.99, 'image': 'https://images.unsplash.com/photo-1494059980473-813e73ee784b?w=500'},
            {'name': 'Stuffed Animal Plush', 'name_es': 'Peluche de Animal', 'price': 19.99, 'image': 'https://images.unsplash.com/photo-1558877385-81a1c7e67d72?w=500'},
            {'name': 'Art Supplies Kit', 'name_es': 'Kit de Suministros de Arte', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500'},
        ],
        'food-beverages': [
            {'name': 'Organic Coffee Beans 1kg', 'name_es': 'Granos de Café Orgánico 1kg', 'price': 24.99, 'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500'},
            {'name': 'Premium Tea Collection', 'name_es': 'Colección de Té Premium', 'price': 29.99, 'image': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500'},
            {'name': 'Dark Chocolate Gift Box', 'name_es': 'Caja de Regalo Chocolate Negro', 'price': 34.99, 'image': 'https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=500'},
            {'name': 'Mixed Nuts Variety Pack', 'name_es': 'Pack Variado de Frutos Secos', 'price': 19.99, 'image': 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=500'},
            {'name': 'Olive Oil Extra Virgin', 'name_es': 'Aceite de Oliva Virgen Extra', 'price': 22.99, 'image': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500'},
            {'name': 'Honey Raw Organic', 'name_es': 'Miel Cruda Orgánica', 'price': 18.99, 'image': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500'},
        ],
    }

    # Coupon data
    COUPONS = [
        {'code': 'WELCOME10', 'discount': 10},
        {'code': 'SAVE20', 'discount': 20},
        {'code': 'FLASH25', 'discount': 25},
        {'code': 'VIP30', 'discount': 30},
        {'code': 'HOLIDAY15', 'discount': 15},
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Coupon.objects.all().delete()

        self.stdout.write(self.style.HTTP_INFO('🚀 Starting data population...'))
        
        # Create categories
        categories = self.create_categories()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(categories)} categories'))

        # Create products
        products = self.create_products(categories)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(products)} products'))

        # Create coupons
        coupons = self.create_coupons()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(coupons)} coupons'))

        # Create sample orders
        orders = self.create_orders(products)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(orders)} sample orders'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database populated successfully!'))
        self.stdout.write(f'   - Categories: {len(categories)}')
        self.stdout.write(f'   - Products: {len(products)}')
        self.stdout.write(f'   - Coupons: {len(coupons)}')
        self.stdout.write(f'   - Orders: {len(orders)}')

    def create_categories(self):
        categories = []
        for cat_data in self.CATEGORIES:
            # Check if category already exists
            existing = Category.objects.filter(
                translations__slug=cat_data['en']['slug'],
                translations__language_code='en'
            ).first()
            
            if existing:
                categories.append(existing)
                continue

            category = Category.objects.create()
            
            # Set English translations
            category.set_current_language('en')
            category.name = cat_data['en']['name']
            category.slug = cat_data['en']['slug']
            category.save()
            
            # Set Spanish translations
            category.set_current_language('es')
            category.name = cat_data['es']['name']
            category.slug = cat_data['es']['slug']
            category.save()
            
            categories.append(category)
        
        return categories

    def create_products(self, categories):
        products = []
        
        for category in categories:
            category.set_current_language('en')
            cat_slug = category.slug
            
            if cat_slug not in self.PRODUCTS:
                continue
                
            for prod_data in self.PRODUCTS[cat_slug]:
                # Check if product already exists
                existing = Product.objects.filter(
                    translations__name=prod_data['name'],
                    translations__language_code='en'
                ).first()
                
                if existing:
                    products.append(existing)
                    continue

                product = Product.objects.create(
                    category=category,
                    price=Decimal(str(prod_data['price'])),
                    available=True,
                )
                
                # Set English translations
                product.set_current_language('en')
                product.name = prod_data['name']
                product.slug = prod_data['name'].lower().replace(' ', '-').replace('&', 'and')[:200]
                product.description = self.generate_description(prod_data['name'])
                product.save()
                
                # Set Spanish translations  
                product.set_current_language('es')
                product.name = prod_data['name_es']
                product.slug = prod_data['name_es'].lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')[:200]
                product.description = self.generate_description_es(prod_data['name_es'])
                product.save()
                
                # Note: For images, we're storing the URL in the description or you can 
                # download them. For simplicity, we'll handle this differently.
                # The image field expects a file, so we'll leave it blank and use 
                # the static no_image.png or you can extend this to download images.
                
                products.append(product)
        
        return products

    def generate_description(self, name):
        descriptions = [
            f"Discover the amazing {name}. This premium product offers exceptional quality and outstanding performance. Perfect for everyday use with modern design and durable construction.",
            f"Introducing the {name} - your perfect companion for a better lifestyle. Crafted with attention to detail and built to last. Experience the difference quality makes.",
            f"The {name} combines style with functionality. Made from premium materials, this product delivers excellent value and reliability. A must-have addition to your collection.",
        ]
        return random.choice(descriptions)

    def generate_description_es(self, name):
        descriptions = [
            f"Descubre el increíble {name}. Este producto premium ofrece calidad excepcional y rendimiento sobresaliente. Perfecto para el uso diario con diseño moderno y construcción duradera.",
            f"Presentamos el {name} - tu compañero perfecto para un mejor estilo de vida. Elaborado con atención al detalle y construido para durar. Experimenta la diferencia que hace la calidad.",
            f"El {name} combina estilo con funcionalidad. Fabricado con materiales premium, este producto ofrece excelente valor y confiabilidad. Una adición imprescindible a tu colección.",
        ]
        return random.choice(descriptions)

    def create_coupons(self):
        coupons = []
        now = timezone.now()
        
        for coup_data in self.COUPONS:
            coupon, created = Coupon.objects.get_or_create(
                code=coup_data['code'],
                defaults={
                    'discount': coup_data['discount'],
                    'valid_from': now - timedelta(days=30),
                    'valid_to': now + timedelta(days=90),
                    'active': True,
                }
            )
            coupons.append(coupon)
        
        return coupons

    def create_orders(self, products):
        orders = []
        
        first_names = ['John', 'Emma', 'Michael', 'Sarah', 'David', 'Lisa', 'James', 'Emily', 'Robert', 'Jennifer']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin']
        
        for i in range(10):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=f'{first_name.lower()}.{last_name.lower()}@example.com',
                address=f'{random.randint(100, 9999)} Main Street',
                postal_code=f'{random.randint(10000, 99999)}',
                city=random.choice(cities),
                paid=random.choice([True, True, False]),  # 66% paid
            )
            
            # Add 1-4 random products to the order
            order_products = random.sample(products, min(random.randint(1, 4), len(products)))
            for product in order_products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=random.randint(1, 3),
                )
            
            orders.append(order)
        
        return orders
