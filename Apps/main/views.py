from django.shortcuts import render
from django.http import request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from .serializers import RequestSerializer
from .utils import get_products_and_materials, get_materials


@api_view(['POST'])
def GetListView(request, *args, **kwargs):
    """
    Example for simple request:

    {
        "order": [
            {
                "product_name": "Ko'ylak",
                "product_qty": 20
            },
            {
                "product_name": "Shim",
                "product_qty": 20
            }
        ]
    }

    """

    # checking request.data is valid
    serializer = RequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    ordered_products, needed_materials = get_products_and_materials(serializer.data['order'])

    materials_in_warehouse = get_materials(needed_materials)

    return Response({'order': "dasd"})
