from django.test import TestCase, Client
from django.urls import reverse
from product.models import Product
from material.models import Material
from product_material.models import Product_Materials
from warehouse.models import Warehouse
import json
import os

class ResponseIsTrue(TestCase):
    def setUp(self):
        # creating products
        p_koylak = Product.objects.create(name="ko'ylak")
        p_shim = Product.objects.create(name="shim")

        # creating materials
        m_mato = Material.objects.create(name="mato")
        m_ip = Material.objects.create(name="ip")
        m_tugma = Material.objects.create(name="tugma")
        m_zamok = Material.objects.create(name="zamok")

        # creating relationship table: Product_Materials
        Product_Materials.objects.create(product=p_koylak, material=m_mato, quantity=0.8)
        Product_Materials.objects.create(product=p_koylak, material=m_tugma, quantity=5)
        Product_Materials.objects.create(product=p_koylak, material=m_ip, quantity=10)
        Product_Materials.objects.create(product=p_shim, material=m_mato, quantity=1.4)
        Product_Materials.objects.create(product=p_shim, material=m_ip, quantity=15)
        Product_Materials.objects.create(product=p_shim, material=m_zamok, quantity=1)

        # creating warehouse table
        Warehouse.objects.create(material=m_mato, remainder=12, price=1500)
        Warehouse.objects.create(material=m_mato, remainder=200, price=1600)
        Warehouse.objects.create(material=m_ip, remainder=40, price=500)
        Warehouse.objects.create(material=m_ip, remainder=300, price=550)
        Warehouse.objects.create(material=m_tugma, remainder=500, price=300)
        Warehouse.objects.create(material=m_zamok, remainder=1000, price=2000)

        self.client = Client()

        return super().setUp()
    

    def test_response_is_true(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'tests', 'test_1_req.json')) as req_file:
                data = json.load(req_file)
        except Exception:
            print(Exception)
            return

        try:
            with open(os.path.join(os.path.dirname(__file__), 'tests', 'test_1_res.json')) as res_file:
                true_response = json.load(res_file)
        except Exception:
            print(Exception)
            return
            
        response = self.client.post(reverse('main:get_list'), data=data, content_type='application/json')
        res = json.loads(response.content)

        self.assertDictEqual(res, true_response)