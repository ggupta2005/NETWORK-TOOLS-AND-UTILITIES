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


    def test_validate_nexthop_ipv4(self):

        # Positive test cases
        self.assertEqual(validate_nexthop_ipv4('1.1.1.2'), True)
        self.assertEqual(validate_nexthop_ipv4('0.0.0.1'), True)
        self.assertEqual(validate_nexthop_ipv4('0.0.0.0'), True)

        # Negative test cases
        self.assertEqual(validate_nexthop_ipv4('1.1.1'), False)
        self.assertEqual(validate_nexthop_ipv4('some string'), False)
        self.assertEqual(validate_nexthop_ipv4('2'), False)
        self.assertEqual(validate_nexthop_ipv4(None), False)


    def test_ipv4_addr_nexthop(self):

        # Positive test cases
        self.assertEqual(validate_nexthop('1.1.1.2'), True)
        self.assertEqual(validate_nexthop('0.0.0.1'), True)
        self.assertEqual(validate_nexthop('2'), True)

        # Negative test cases
        self.assertEqual(validate_nexthop('1.1.1'), False)
        self.assertEqual(validate_nexthop('0.0.0.1'), True)
        self.assertEqual(validate_nexthop('some string'), False)
   

if __name__ == '__main__':
    unittest.main()
