import sys
import socket


IPV4_MIN_OCTET_NUMBER = 1
IPV4_MAX_OCTET_NUMBER = 200
IPV6_MIN_OCTET_NUMBER = 1
IPV6_MAX_OCTET_NUMBER = 9999

ILLEGAL_INTERFACE = 0


def get_tool_usage_string():
    
    return ("Usage: python ipv4_route_gen.py " +  
            "<number of routes> <address-family> " + 
            "<nexthop1> <nexthop2>...")


def get_ipv4_static_route_config_string(**kwargs):

    first_octet = str(kwargs.get('first_octet', None))
    second_octet = str(kwargs.get('second_octet', None))
    third_octet = str(kwargs.get('third_octet', None))
    fourth_octet = str(kwargs.get('fourth_octet', None))
    if_ipv4 = str(kwargs.get('if_ipv4', False))

    nexthop = str(kwargs.get('nexthop', None))

    if first_octet is None or second_octet is None or \
       third_octet is None or fourth_octet is None or \
       nexthop is None:
        return None

    if if_ipv4 is True:
        route_string = 'ip route %s.%s.%s.%s/%s %s' %(first_octet,
                       second_octet, third_octet, fourth_octet , '32',
                       nexthop)
    else:
        route_string = 'ipv6 route %s:%s:%s:%s::1/%s %s' %(first_octet,
                       second_octet, third_octet, fourth_octet , '128',
                       nexthop)

    return route_string


def get_static_ipv4_route_by_count(if_ipv4, count, nexthop_list):

    route_count = int(count)

    if route_count <= 0:
        return

    if if_ipv4 is not True and if_ipv4 is not False:
        return

    if nexthop_list is None:
        return

    if len(nexthop_list) == 0:
        return

    min_number = IPV4_MIN_OCTET_NUMBER
    max_number = IPV4_MAX_OCTET_NUMBER + 1

    if if_ipv4 is False:
        min_number = IPV6_MIN_OCTET_NUMBER
        max_number = IPV6_MAX_OCTET_NUMBER + 1

    total_routes = 0
    for first_octet in range(min_number, max_number):
        for second_octet in range(min_number, max_number):
            for third_octet in range(min_number, max_number):
                for fourth_octet in range(min_number, max_number):

                    if total_routes >= route_count:
                        break

                    for nexthop_index in range(0, len(nexthop_list)):

                        route_string = get_ipv4_static_route_config_string(
                                            first_octet=first_octet,
                                            second_octet=second_octet,
                                            third_octet=third_octet,
                                            fourth_octet=fourth_octet,
                                            if_ipv4=if_ipv4,
                                            nexthop=nexthop_list[nexthop_index])

                        if route_string is None:
                            return

                        print route_string

                    total_routes = total_routes + 1

                if total_routes >= route_count:
                    break

            if total_routes >= route_count:
                break

        if total_routes >= route_count:
            break


def validate_route_count(count):

    if count is None:
        return False

    count_in_integer = int(count)

    if count_in_integer <= 0:
        return False

    return True


def validate_address_family(address_family):
    if address_family is None:
        return False

    if address_family.lower() == "IPv4".lower():
        return True

    if address_family.lower() == "IPv6".lower():
        return True

    return False


def if_address_family_is_ipv4(address_family):
    if address_family is None:
        return False

    if address_family.lower() == "IPv4".lower():
        return True

    return False


def if_address_family_is_ipv6(address_family):
    if address_family is None:
        return False

    if address_family.lower() == "IPv6".lower():
        return True

    return False


def validate_interface_name(interface_name):
    if interface_name is None:
        return False

    try:
        some_int = int(interface_name)
    
        if some_int <= ILLEGAL_INTERFACE:
            return False
    except:
        return False

    return True


def validate_nexthop_ipv4(nexthop_ipv4):
    if nexthop_ipv4 is None:
        return False

    try:
        socket.inet_pton(socket.AF_INET, nexthop_ipv4)

    except:
        return False

    return True


def validate_nexthop_ipv6(nexthop_ipv6):
    if nexthop_ipv6 is None:
        return False

    try:
        socket.inet_pton(socket.AF_INET6, nexthop_ipv6)

    except:
        return False

    return True


def validate_nexthop(nexthop):

    if nexthop is None:
        return False
    
    if validate_nexthop_ipv6(nexthop) is True:
        return True

    if validate_nexthop_ipv4(nexthop) is True:
        return True

    if validate_interface_name(nexthop) is True:
        return True

    return False


if __name__ == '__main__':
    print 'Number of arguments: ' + str(len(sys.argv))

    if len(sys.argv) < 3:

        print get_tool_usage_string()
        
    else:

        nexthop_list = []

        if validate_route_count(sys.argv[1]) is False:
            print get_tool_usage_string()
            assert False, "Invalid value of number of routes!!!"

        route_count = sys.argv[1]

        if validate_address_family(sys.argv[2]) is False:
            print get_tool_usage_string()
            assert False, "Invalid address family!!!"

        if_ipv4 = if_address_family_is_ipv4(sys.argv[2])

        for nexthop_index in range(3, (len(sys.argv))):
            if validate_nexthop(sys.argv[nexthop_index]) is False:
                print get_tool_usage_string()
                assert False, "Invalid nexthop " + sys.argv[nexthop_index] + "!!!"

            nexthop_list.append(sys.argv[nexthop_index])

        print nexthop_list
        get_static_ipv4_route_by_count(if_ipv4, route_count, nexthop_list)

