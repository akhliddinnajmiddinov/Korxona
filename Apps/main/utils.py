from .serializers import ProductQuantitySerializer
from django.shortcuts import get_object_or_404
from typing import List, Tuple
from queue import Queue

from product.models import Product
from product_material.models import Product_Materials
from warehouse.models import Warehouse

def get_products_and_materials(ordered_products: List[dict]) -> Tuple[List[dict], List[str]]:
    """This function checks all the given ordered products are valid and 
    collects materials that needed to make these products""" 

    needed_materials = set()

    for product in ordered_products:
        serializer = ProductQuantitySerializer(data=product)
        serializer.is_valid(raise_exception=True)

        product['product'] = get_object_or_404(Product, name=product['product_name'].lower())
        product['materials'] = Product_Materials.objects.filter(product=product['product'])
        
        needed_materials = needed_materials.union([rel.material.name for rel in product['materials']])

        del product['product_name']

    return ordered_products, needed_materials


def get_materials(needed_materials: List[str]) -> dict[str, List[dict]]:
    res = {}

    for needed_material in needed_materials:
        res[needed_material] = []
        for rel in Warehouse.objects.filter(material__name = needed_material).order_by('-pk'):
            res[needed_material].append({
                'warehouse_id': rel.pk,
                'remainder': rel.remainder,
                'price': rel.price
            })

    return res