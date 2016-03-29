import unittest
from static_route_config_generator import *


class test_static_route_config_generator(unittest.TestCase):


    def test_if_address_family_is_ipv4(self):

        # Positive test cases
        self.assertEqual(if_address_family_is_ipv4("ipv4"), True)
        self.assertEqual(if_address_family_is_ipv4("iPv4"), True)
        self.assertEqual(if_address_family_is_ipv4("IPV4"), True)

        # Negative test cases
        self.assertEqual(if_address_family_is_ipv4(None), False)
        self.assertEqual(if_address_family_is_ipv4('ip'), False)
        self.assertEqual(if_address_family_is_ipv4('some string'), False)
        self.assertEqual(if_address_family_is_ipv4("ipv6"), False)
        self.assertEqual(if_address_family_is_ipv4("iPv6"), False)
        self.assertEqual(if_address_family_is_ipv4("IPV6"), False)


    def test_if_address_family_is_ipv6(self):

        # Positive test cases
        self.assertEqual(if_address_family_is_ipv6("ipv6"), True)
        self.assertEqual(if_address_family_is_ipv6("iPv6"), True)
        self.assertEqual(if_address_family_is_ipv6("IPV6"), True)

        # Negative test cases
        self.assertEqual(if_address_family_is_ipv6(None), False)
        self.assertEqual(if_address_family_is_ipv6('ip'), False)
        self.assertEqual(if_address_family_is_ipv6('some string'), False)
        self.assertEqual(if_address_family_is_ipv6("ipv4"), False)
        self.assertEqual(if_address_family_is_ipv6("iPv4"), False)
        self.assertEqual(if_address_family_is_ipv6("IPV4"), False)


    def test_validate_address_family(self):

        # Positive test cases
        self.assertEqual(validate_address_family("ipv4"), True)
        self.assertEqual(validate_address_family("ipv6"), True)
        self.assertEqual(validate_address_family("iPv4"), True)
        self.assertEqual(validate_address_family("iPv6"), True)
        self.assertEqual(validate_address_family("IPV4"), True)
        self.assertEqual(validate_address_family("IPV6"), True)

        # Negative test cases
        self.assertEqual(validate_address_family(None), False)
        self.assertEqual(validate_address_family("ip"), False)
        self.assertEqual(validate_address_family("some string"), False)


    def test_validate_interface_name(self):

        # Positive test cases
        self.assertEqual(validate_interface_name('1'), True)
        self.assertEqual(validate_interface_name('100'), True)

        # Negative test cases
        self.assertEqual(validate_interface_name(None), False)
        self.assertEqual(validate_interface_name("some string"), False)
        self.assertEqual(validate_interface_name('1.1'), False)
        self.assertEqual(validate_interface_name('0'), False)
        self.assertEqual(validate_interface_name('-1'), False)
        self.assertEqual(validate_interface_name('1.1.1.2'), False)
        self.assertEqual(validate_interface_name('111:111::1'), False)


    def test_validate_nexthop_ipv4(self):

        # Positive test cases
        self.assertEqual(validate_nexthop_ipv4('1.1.1.2'), True)
        self.assertEqual(validate_nexthop_ipv4('0.0.0.1'), True)
        self.assertEqual(validate_nexthop_ipv4('0.0.0.0'), True)

        # Negative test cases
        self.assertEqual(validate_nexthop_ipv4(None), False)
        self.assertEqual(validate_nexthop_ipv4('1.1.1'), False)
        self.assertEqual(validate_nexthop_ipv4('some string'), False)
        self.assertEqual(validate_nexthop_ipv4('2'), False)
        self.assertEqual(validate_nexthop_ipv4('111:111::1'), False)


    def test_validate_nexthop_ipv6(self):

        # Positive test cases
        self.assertEqual(validate_nexthop_ipv6('111:111::1'), True)
        self.assertEqual(validate_nexthop_ipv6('1::1'), True)
        self.assertEqual(validate_nexthop_ipv6('0::'), True)

        # Negative test cases
        self.assertEqual(validate_nexthop_ipv6(None), False)
        self.assertEqual(validate_nexthop_ipv6('111::111::111'), False)
        self.assertEqual(validate_nexthop_ipv6('some string'), False)
        self.assertEqual(validate_nexthop_ipv6('2'), False)
        self.assertEqual(validate_nexthop_ipv6('1.1.1.1'), False)


    def test_validate_nexthop(self):

        # Positive test cases
        self.assertEqual(validate_nexthop('1.1.1.2'), True)
        self.assertEqual(validate_nexthop('2'), True)
        self.assertEqual(validate_nexthop('111:111::1'), True)

        # Negative test cases
        self.assertEqual(validate_nexthop(None), False)
        self.assertEqual(validate_nexthop('1.1.1'), False)
        self.assertEqual(validate_nexthop('some string'), False)
        self.assertEqual(validate_nexthop('111::111::111'), False)
        self.assertEqual(validate_nexthop('-1'), False)
        self.assertEqual(validate_nexthop('0'), False)


    def test_validate_route_count(self):

        # Positive test cases
        self.assertEqual(validate_route_count('1'), True)
        self.assertEqual(validate_route_count('10'), True)
        self.assertEqual(validate_route_count('100'), True)
        self.assertEqual(validate_route_count(str(MAXIMUM_STATIC_ROUTES)), True)

        # Negative test cases
        self.assertEqual(validate_route_count(None), False)
        self.assertEqual(validate_route_count('0'), False)
        self.assertEqual(validate_route_count('-1'), False)
        self.assertEqual(validate_route_count(str(MAXIMUM_STATIC_ROUTES + 1)), False)


    def test_get_ipv4_static_route_config_string(self):

        # Positive test cases
        static_route_config = get_static_route_config_string(
                                    first_octet='123', second_octet='0',
                                    third_octet='0', fourth_octet='1',
                                    if_ipv4=True, nexthop='1.1.1.5')
        self.assertEqual(static_route_config,
                                    'ip route 123.0.0.1/32 1.1.1.5')

        static_route_config = get_static_route_config_string(
                                    first_octet='123', second_octet='0',
                                    third_octet='0', fourth_octet='1',
                                    if_ipv4=True, nexthop='5')
        self.assertEqual(static_route_config,
                                    'ip route 123.0.0.1/32 5')

        static_route_config = get_static_route_config_string(
                                    first_octet='123', second_octet='0',
                                    third_octet='0', fourth_octet='1',
                                    if_ipv4=False, nexthop='111:111::1')
        self.assertEqual(static_route_config,
                                'ipv6 route 123:0:0:1::1/128 111:111::1')

        static_route_config = get_static_route_config_string(
                                    first_octet='123', second_octet='0',
                                    third_octet='0', fourth_octet='1',
                                    if_ipv4=False, nexthop='1')
        self.assertEqual(static_route_config,
                                'ipv6 route 123:0:0:1::1/128 1')

        # Negative test cases
        static_route_config = get_static_route_config_string(
                                    first_octet=None, second_octet=None,
                                    third_octet=None, fourth_octet=None,
                                    if_ipv4=None, nexthop=None)
        self.assertEqual(static_route_config, None)

        static_route_config = get_static_route_config_string(
                                    first_octet='3', second_octet='3',
                                    third_octet='0', fourth_octet=None,
                                    if_ipv4=True, nexthop='45')
        self.assertEqual(static_route_config, None)

        static_route_config = get_static_route_config_string(
                                    first_octet='3', second_octet='3',
                                    third_octet=None, fourth_octet='6',
                                    if_ipv4=True, nexthop='45')
        self.assertEqual(static_route_config, None)

        static_route_config = get_static_route_config_string(
                                    first_octet='Gaurav',
                                    second_octet='Saurabh',
                                    third_octet='Suresh',
                                    fourth_octet='Amita',
                                    if_ipv4=True, nexthop='Neha')
        self.assertEqual(static_route_config, None)

if __name__ == '__main__':
    unittest.main()
