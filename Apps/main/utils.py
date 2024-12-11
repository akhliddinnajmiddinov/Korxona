from .serializers import ProductQuantitySerializer
from django.shortcuts import get_object_or_404
from typing import List, Tuple
from queue import Queue

from product.models import Product
from product_material.models import Product_Materials
from warehouse.models import Warehouse

import json

def get_products_and_materials(ordered_products: List[dict]) -> Tuple[List[dict], List[str]]:
    """
        This function checks all the given ordered products are valid and 
        collects materials that needed to make these products
    """ 

    # We need needed_materials for getting only required materials from warehouse
    needed_materials = set()

    for product in ordered_products:
        # Checking product is in valid format
        serializer = ProductQuantitySerializer(data=product)
        serializer.is_valid(raise_exception=True)

        # getting materials that we need to make this product
        product_obj = get_object_or_404(Product, name=product['product_name'].lower())
        product['materials'] = Product_Materials.objects.filter(product=product_obj)
        
        # adding materials to needed_materials
        needed_materials = needed_materials.union([material.material.name for material in product['materials']])

    return ordered_products, needed_materials


def get_materials(needed_materials: List[str]) -> dict[str, List[dict]]:
    """
        This function collects all materials we need and returns it.
        Return format: 
        {
            "mato": [
                { "warehouse_id": 2, "remainder": 200.0, "price": 1600 },
                { "warehouse_id": 1, "remainder": 12.0, "price": 1500 }
            ],
            "zamok": [
                ...
            ],
            ...
        }
    """

    # res is just dictionary and it contains lists and dictionaries, as value.
    # That is why it doesn't affect to the database
    res = {}

    for needed_material in needed_materials:
        
        res[needed_material] = []

        # filtering needed_material from warehouse, ordering it in reverse order 
        # to maintain queue DS with list(later we will get 
        # materials from the end in O(1) Time Complexity)


        for material in Warehouse.objects.filter(material__name = needed_material).order_by('-pk'):
            res[needed_material].append({
                'warehouse_id': material.pk,
                'remainder': material.remainder,
                'price': material.price
            })

    return res


def get_needed_materials(ordered_products: List[dict], materials_in_warehouse: dict[str, List[dict]]) -> dict:
    res = {
        'result': []
    }

    for product in ordered_products:
        single_res = {
            'product_name': product['product_name'].capitalize(),
            'product_qty': product['product_qty'],
            'product_materials': []
        }

        # iterating through all materials that we need to make this product
        for material in product['materials']:
            # calculating how much material we need from warehouse
            quantity = product['product_qty'] * material.quantity
            
            m_name = material.material.name

            # while quantity is positive and there are materials we need in warehouse
            while materials_in_warehouse[m_name] and quantity > 0:
                # getting min between quantity and material quantity in the warehouse
                mn_qty = min(quantity, materials_in_warehouse[m_name][-1]['remainder'])
                quantity -= mn_qty

                # subtracting mn_qty from material quantity in warehouse
                # if it is empty we will delete it later
                materials_in_warehouse[m_name][-1]['remainder'] -= mn_qty

                # appending information to single_res about materials we are getting from warehouse
                single_res['product_materials'].append({
                    'warehouse_id': materials_in_warehouse[m_name][-1]['warehouse_id'],
                    'material_name': m_name.capitalize(),
                    'qty': mn_qty,
                    'price': materials_in_warehouse[m_name][-1]['price']
                })

                # if materials run out, we will delete this materials box
                if materials_in_warehouse[m_name][-1]['remainder'] == 0:
                    materials_in_warehouse[m_name].pop()
            
            # If there is some materials we need, we will add it to singe_res with None values
            if quantity > 0:
                single_res['product_materials'].append({
                    'warehouse_id': None,
                    'material_name': m_name.capitalize(),
                    'qty': quantity,
                    'price': None
                })
        
        # adding single result for one product to result
        res['result'].append(single_res)

    return res