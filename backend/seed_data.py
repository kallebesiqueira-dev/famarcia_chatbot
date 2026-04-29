"""
Script di seed per popolare il database con dati di esempio.
Eseguire con: python manage.py shell < seed_data.py
Oppure: python manage.py runscript seed_data (con django-extensions)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pharmacy.models import Product

# Prodotti di esempio realistici per una farmacia italiana
PRODUCTS = [
    {
        'name': 'Tachipirina 1000mg',
        'description': 'Paracetamolo in compresse. Antipiretico e analgesico per febbre e dolori.',
        'price': 4.50,
        'available': True,
        'category': 'farmaco',
        'sku': 'TACH-1000',
        'requires_prescription': False,
    },
    {
        'name': 'Moment 200mg',
        'description': 'Ibuprofene in capsule molli. Per mal di testa, dolori mestruali e muscolari.',
        'price': 7.90,
        'available': True,
        'category': 'farmaco',
        'sku': 'MOM-200',
        'requires_prescription': False,
    },
    {
        'name': 'Aspirina 500mg',
        'description': 'Acido acetilsalicilico. Analgesico, antipiretico e antinfiammatorio.',
        'price': 5.20,
        'available': True,
        'category': 'farmaco',
        'sku': 'ASP-500',
        'requires_prescription': False,
    },
    {
        'name': 'Maalox Plus',
        'description': 'Antiacido per bruciore di stomaco, acidità e digestione lenta.',
        'price': 8.90,
        'available': True,
        'category': 'farmaco',
        'sku': 'MAAL-PLUS',
        'requires_prescription': False,
    },
    {
        'name': 'Enterogermina 2 Miliardi',
        'description': 'Fermenti lattici per riequilibrare la flora intestinale.',
        'price': 10.50,
        'available': True,
        'category': 'farmaco',
        'sku': 'ENTG-2B',
        'requires_prescription': False,
    },
    {
        'name': 'Voltaren Emulgel 2%',
        'description': 'Gel antinfiammatorio per dolori muscolari e articolari.',
        'price': 12.30,
        'available': True,
        'category': 'farmaco',
        'sku': 'VOLT-2',
        'requires_prescription': False,
    },
    {
        'name': 'Rinazina Spray Nasale',
        'description': 'Decongestionante nasale per raffreddore e sinusite.',
        'price': 6.80,
        'available': True,
        'category': 'farmaco',
        'sku': 'RINAZ-SP',
        'requires_prescription': False,
    },
    {
        'name': 'Vicks MediNait Sciroppo',
        'description': 'Sciroppo per tosse, raffreddore e influenza. Azione notturna.',
        'price': 11.90,
        'available': False,
        'category': 'farmaco',
        'sku': 'VICKS-MN',
        'requires_prescription': False,
    },
    {
        'name': 'Vitamina C 1000mg Efferc.',
        'description': 'Integratore di Vitamina C in compresse effervescenti. Supporto sistema immunitario.',
        'price': 8.50,
        'available': True,
        'category': 'integratore',
        'sku': 'VITC-1000',
        'requires_prescription': False,
    },
    {
        'name': 'Magnesio Supremo',
        'description': 'Integratore di magnesio in polvere. Per stanchezza e stress.',
        'price': 14.90,
        'available': True,
        'category': 'integratore',
        'sku': 'MGSUP-300',
        'requires_prescription': False,
    },
    {
        'name': 'Melatonina 1mg',
        'description': 'Integratore per favorire il sonno. 60 compresse.',
        'price': 9.90,
        'available': True,
        'category': 'integratore',
        'sku': 'MELAT-1',
        'requires_prescription': False,
    },
    {
        'name': 'Crema Solare SPF50+',
        'description': 'Protezione solare molto alta. Adatta a pelli sensibili.',
        'price': 18.90,
        'available': True,
        'category': 'cosmetico',
        'sku': 'SOLAR-50',
        'requires_prescription': False,
    },
    {
        'name': 'Crema Idratante Corpo',
        'description': 'Crema idratante per pelle secca. Con acido ialuronico.',
        'price': 15.50,
        'available': True,
        'category': 'cosmetico',
        'sku': 'CREAM-ID',
        'requires_prescription': False,
    },
    {
        'name': 'Termometro Digitale',
        'description': 'Termometro digitale con display LCD. Lettura rapida e precisa.',
        'price': 9.90,
        'available': True,
        'category': 'dispositivo',
        'sku': 'TERM-DIG',
        'requires_prescription': False,
    },
    {
        'name': 'Misuratore Pressione Digitale',
        'description': 'Sfigmomanometro digitale da braccio. Con memoria 60 misurazioni.',
        'price': 45.00,
        'available': True,
        'category': 'dispositivo',
        'sku': 'PRESS-DIG',
        'requires_prescription': False,
    },
    {
        'name': 'Amoxicillina 1g',
        'description': 'Antibiotico a largo spettro. RICHIEDE RICETTA MEDICA.',
        'price': 6.50,
        'available': True,
        'category': 'farmaco',
        'sku': 'AMOX-1G',
        'requires_prescription': True,
    },
]


def seed_products():
    """Popola il database con i prodotti di esempio."""
    created_count = 0
    updated_count = 0

    for product_data in PRODUCTS:
        product, created = Product.objects.update_or_create(
            sku=product_data['sku'],
            defaults=product_data,
        )
        if created:
            created_count += 1
            print(f"  ✅ Creato: {product.name}")
        else:
            updated_count += 1
            print(f"  🔄 Aggiornato: {product.name}")

    print(f"\n{'='*50}")
    print(f"Seed completato: {created_count} creati, {updated_count} aggiornati")
    print(f"Totale prodotti nel database: {Product.objects.count()}")


if __name__ == '__main__':
    print("🌱 Avvio seed database prodotti farmacia...\n")
    seed_products()
