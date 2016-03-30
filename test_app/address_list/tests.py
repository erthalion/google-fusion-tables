from django.test import TestCase

import mock
from rest_framework.test import APIRequestFactory
from address_list.views import AddressView


class AddressApiTestCase(TestCase):
    def test_no_address(self):
        with mock.patch('address_list.utils.get_address', return_value=None):
            factory = APIRequestFactory()
            request = factory.post(
                '/api/address',
                {
                    'latitude': '0.0',
                    'longitude': '0.0'
                }
            )

            response = AddressView.as_view()(request)
            self.assertEqual(response.status_code, 400)
