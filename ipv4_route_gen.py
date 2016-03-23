import sys
import socket

def get_static_ipv4_route_by_count(count, nexthop_list):

    route_count = int(count)

    if route_count <= 0:
        return

    if nexthop_list is None:
        return

    if len(nexthop_list) == 0:
        return

    total_routes = 0
    for first_octet in range(1, 200):
        for second_octet in range(0, 200):
            for third_octet in range(0, 200):
                for fourth_octet in range(0, 200):

                    if total_routes >= route_count:
                        break

                    for nexthop_index in range(0, len(nexthop_list)):
                        route_string = 'ip route %s.%s.%s.%s/%s %s' %(str(first_octet),
                                       str(second_octet), str(third_octet), str(fourth_octet) , '32',
                                       nexthop_list[nexthop_index])

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


def validate_interface_name(interface_name):
    if interface_name is None:
        return False

    if '.' in interface_name:
        return False

    return True


def validate_nexthop(nexthop):

    if nexthop is None:
        return False

    try:
        socket.inet_pton(socket.AF_INET, nexthop)

    except:

        try:
            socket.inet_pton(socket.AF_INET6, nexthop)

        except:
            if validate_interface_name(nexthop) is False:
                return False

    return True


if __name__ == '__main__':
    print 'Number of arguments: ' + str(len(sys.argv))

    if len(sys.argv) < 3:

        print "Usage: python ipv4_route_gen.py <number of routes> <nexthop1> <nexthop2>..."

    else:

        nexthop_list = []

        if validate_route_count(sys.argv[1]) is False:
            assert False, "Invalid value of number of routes!!!"
            #return

        route_count = sys.argv[1]

        for nexthop_index in range(2, (len(sys.argv))):
            if validate_nexthop(sys.argv[nexthop_index]) is False:
                assert False, "Invalid nexthop " + sys.argv[nexthop_index] + "!!!"
                #return

            nexthop_list.append(sys.argv[nexthop_index])

        print nexthop_list
        get_static_ipv4_route_by_count(route_count, nexthop_list)

