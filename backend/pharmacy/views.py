"""
Views per l'app Pharmacy.
API per la gestione del catalogo prodotti.
"""
import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer, ProductListSerializer

logger = logging.getLogger('pharmacy')


@api_view(['GET'])
def product_list(request):
    """
    GET /api/products/
    
    Lista prodotti con filtri opzionali.
    
    Query params:
        ?available=true       - Solo prodotti disponibili
        ?category=farmaco     - Filtra per categoria
        ?search=paracetamolo  - Cerca per nome
    """
    queryset = Product.objects.all()

    # Filtro disponibilità
    available = request.query_params.get('available')
    if available is not None:
        queryset = queryset.filter(available=available.lower() == 'true')

    # Filtro categoria
    category = request.query_params.get('category')
    if category:
        queryset = queryset.filter(category=category)

    # Ricerca per nome
    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(name__icontains=search)

    serializer = ProductListSerializer(queryset, many=True)

    return Response({
        'count': queryset.count(),
        'results': serializer.data,
    })


@api_view(['GET'])
def product_detail(request, pk):
    """
    GET /api/products/<id>/
    
    Dettaglio singolo prodotto.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Prodotto non trovato'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def product_search(request):
    """
    GET /api/products/search/?q=paracetamolo
    
    Ricerca avanzata prodotti.
    """
    query = request.query_params.get('q', '').strip()

    if not query or len(query) < 2:
        return Response(
            {'error': 'Inserisci almeno 2 caratteri per la ricerca'},
            status=status.HTTP_400_BAD_REQUEST
        )

    products = Product.objects.filter(
        name__icontains=query,
        available=True,
    )

    serializer = ProductListSerializer(products, many=True)

    return Response({
        'query': query,
        'count': products.count(),
        'results': serializer.data,
    })
