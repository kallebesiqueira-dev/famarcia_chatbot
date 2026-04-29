"""
Modelli per l'app Pharmacy.
Gestisce il catalogo prodotti della farmacia.
"""
from django.db import models


class Product(models.Model):
    """
    Prodotto disponibile in farmacia.
    Modello base predisposto per estensioni future (categorie, immagini, etc.).
    """
    CATEGORY_CHOICES = [
        ('farmaco', 'Farmaco'),
        ('integratore', 'Integratore'),
        ('cosmetico', 'Cosmetico'),
        ('dispositivo', 'Dispositivo Medico'),
        ('igiene', 'Igiene Personale'),
        ('altro', 'Altro'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Nome Prodotto',
        db_index=True,
    )
    description = models.TextField(
        verbose_name='Descrizione',
        blank=True,
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Prezzo (€)',
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Disponibile',
        db_index=True,
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='farmaco',
        verbose_name='Categoria',
        db_index=True,
    )
    # Campi aggiuntivi per completezza
    sku = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Codice SKU',
        unique=True,
        null=True,
    )
    requires_prescription = models.BooleanField(
        default=False,
        verbose_name='Richiede Ricetta',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data Inserimento',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Ultimo Aggiornamento',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Prodotto'
        verbose_name_plural = 'Prodotti'
        indexes = [
            models.Index(fields=['category', 'available']),
            models.Index(fields=['name', 'available']),
        ]

    def __str__(self):
        status_icon = '✅' if self.available else '❌'
        return f"{status_icon} {self.name} - €{self.price}"
