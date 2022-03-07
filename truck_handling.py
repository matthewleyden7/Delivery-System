# Matthew Leyden
# Student ID: 001008459
# Data Structures and Algorithms 2

from package_handling import prepare_packages, prepare_distance_graph
import string
from datetime import timedelta, datetime
from truck import truck

# use a greedy path algorithm to take the trucks original route and find a better one.
def find_greedy_route(route):


    # truck starts at the station
    station = "4001 S 700 E"

    # route_copy is a copy of the trucks original route minus station
    route_copy = [addr for addr in route if addr != "4001 S 700 E"]
    path_greedy = [station]

    while route_copy != []:
        # keep track of the minimum edge and therefore closest address
        min_value = (0.0, station)

        for address in route_copy:
            # get the distance from previous address to next address using the graph.edges
            distance = graph.edges[path_greedy[-1], address]

            if min_value[0] == 0.0:
                min_value = (distance, address)

            # if the distance is less than the previous min_value, distance becomes the new min_value
            if distance < min_value[0] and distance != 0.0:
                min_value = (distance, address)

        # make sure that the address is not already in path_greedy to avoid going to same location twice.
        if min_value[1] not in path_greedy:
            path_greedy.append(min_value[1])
        # remove address and continue until route_copy is empty.
        route_copy.remove(min_value[1])
    # Append WGUPS at end to finish route
    path_greedy.append("4001 S 700 E" )
    return path_greedy

def get_routes():

    # Use greedy algorithm to find better route
    truck1.route = find_greedy_route(truck1.route)
    truck2.route = find_greedy_route(truck2.route)
    find_deadline = [pkg for pkg in truck2.packages if pkg[5] == '10:30']
    if find_deadline != []:
        addrs = [c[1] for c in find_deadline]
        for addr in addrs:
            truck2.route.remove(addr)
            truck2.route.insert(1, addr)
    truck3.route = find_greedy_route(truck3.route)


def truck_packages_information():

    # neatly print package information for each truck using the print_truck_packages_info function from the truck class
    print('Package information for {}'.format(truck1.name))
    truck1.print_truck_packages_info()
    print('Total packages:  {}'.format(len(truck1.packages)))
    print()
    print('Package information for {}'.format(truck2.name))
    truck2.print_truck_packages_info()
    print('Total packages:  {}'.format(len(truck2.packages)))
    print()
    print('Package information for {}'.format(truck3.name))
    truck3.print_truck_packages_info()
    print('Total packages:  {}'.format(len(truck3.packages)))
    print()

def total_miles():
    # since the miles traveled by each truck was consistently updated in the deliver function, simply print to screen.
    print('MILES TRAVELED = {} = {} --- {} = {} --- {} = {}\nTotal miles traveled by all 3 trucks = {}'.format(truck1.name, round(truck1.miles_traveled, 1), truck2.name,
    round(truck2.miles_traveled, 1), truck3.name, round(truck3.miles_traveled, 1), round(truck1.miles_traveled + truck2.miles_traveled + truck3.miles_traveled, 1)))

def sort_packages(package_list, truck_groups):
    # first check if package id is in the list of truck ids that need to go together. the next 3 will search whether an
    # address is already in a particular truck to avoid going to same address at 2 different times. the last 3 place
    # packages on trucks as long as they have not exceeded the maximum payload  O(N)
    for pkg in package_list:
        if pkg[0] in truck_groups:

            if len(truck1.packages) == 16:
                pkg_replace = [item for item in truck1.packages if item[7] == '' and item[5] == '17:00'][0]
                truck1.packages.remove(pkg_replace)
                if len(truck2.packages) < 16:
                    truck2.packages.append(pkg_replace)
                else:
                    truck3.packages.append(pkg_replace)
            truck1.insert_pkg(pkg)
        elif pkg[1] in truck1.route and len(truck1.packages) < truck1.max_payload and pkg[5] == '17:00':
            truck1.insert_pkg(pkg)
        elif pkg[1] in truck2.route and len(truck2.packages) < truck2.max_payload and pkg[5] == '17:00':
            truck2.insert_pkg(pkg)
        elif pkg[1] in truck3.route and len(truck3.packages) < truck3.max_payload and pkg[5] == '17:00':
            truck3.insert_pkg(pkg)

        elif len(truck1.packages) < truck1.max_payload:
            truck1.insert_pkg(pkg)
        elif len(truck2.packages) < truck2.max_payload:
            truck2.insert_pkg(pkg)
        elif len(truck3.packages) < truck3.max_payload:
            truck3.insert_pkg(pkg)
        else:
            print('Not enough room on trucks')

def load_trucks():

    # Here we sort the packages based on importance. packages with special notes go into special_packages, packages
    # that have a deadline earlier than end of day go into priority packages, and the rest go into regular_packages O(N^2)
    special_packages = []
    priority_packages = []
    regular_packages = []
    for address in graph.address_list:
        for pkg in graph.vertices[address]:
            if pkg[7] != '':
                special_packages.append(pkg)
            elif pkg[5] != '17:00':
                priority_packages.append(pkg)
            else:
                regular_packages.append(pkg)

    truck_groups = []
    max_delay = datetime(2020, 10, 20, 8, 0, 0)
    # start loading special packages first O(N)
    for pkg in special_packages:
        # If package must go on specific truck, parse truck number and place on appropriate truck by name
        # (Even though truck 2 is only requirement, will work with different trucks)
        if 'Must be on' in pkg[7] or 'on truck' in pkg[7]:
            truck_match = [key for key in list(trucks.keys()) if key in pkg[7].lower()]

            if truck_match != []:
                trucks[truck_match[0]].insert_pkg(pkg)


        # If special note requires package to be on same truck as certain others, parse integer id's from string and store id's for later reference
        elif 'must be with' in pkg[7].lower() or 'be delivered with' in pkg[7].lower():
            pkg_ids = [i for i in [word.strip(string.punctuation) for word in pkg[7].split()] if i.isdigit()]
            truck_groups.extend(pkg_ids)
            truck1.insert_pkg(pkg)


        # For packages that have been delayed, they are put onto truck 2 which will take off at a later hour (9:05)
        elif 'delayed' in pkg[7].lower():
            # parse hours and minutes from string
            hours, minutes = map(int, pkg[7].split()[-1].split(':'))

            # convert the hours and minutes to date time. if the time delay is less than 10:00 (which it is normally) we
            # will delay truck 2's start time until then. If it's later, it will wait until truck 3.
            time_delay = datetime(2020, 10, 20, hours, minutes, 0)

            if time_delay >= max_delay and  time_delay < datetime(2020, 10, 20, 10, 0, 0):
                max_delay = time_delay
                truck2.time_delay = time_delay
                truck2.reset()
                truck2.insert_pkg(pkg)
            elif time_delay > max_delay:
                max_delay = time_delay
                truck3.time_delay = time_delay
                truck3.reset()
                truck3.insert_pkg(pkg)
            else:
                truck2.insert_pkg(pkg)

        # The one package that has a wrong address that will be updated later will go on truck 3 which will be the last
        # to leave.
        elif 'wrong address' in pkg[7].lower():
            truck3.insert_pkg(pkg)

        else:
            truck2.insert_pkg(pkg)

    # priority_packages and regular packages are loaded with the same method, which will fill the earlier trucks first.
    sort_packages(priority_packages, truck_groups)
    sort_packages(regular_packages, truck_groups)

# This function takes a time that user requested, traverses the predefined truck routes while calculating the distances between the
# addresses using the graphs edges as well as the time in minutes to make each trip and updating the status as it goes.  O(N^2)
def deliver(truck_name, time_stamp):

    truck = trucks[truck_name]
    truck.reset()
    distances = graph.edges

    # first determine whether or not the truck has left the WGUPS station. truck1 leaves at 8 am sharp because it has
    # most of the earliest deadline packages. truck 2 will leave at the latest delayed time (which is normally 9:05 but
    # can be changed by user), and truck 3 will not leave until truck 1 returns because there are only 2 drivers.
    start = (truck.time_delay if truck.name != 'truck 3' else truck1.finish)
    truck.time = start
    location = ('at the station' if start > time_stamp else 'left the station at {}'.format(start.time()))
    # establish a next package and next estimated arrival for trucks that don't leave the station before time_stamp.
    next_address = truck.route[1]
    next_est_arrival = truck.time + timedelta(minutes=distances[truck.route[0], truck.route[1]] / truck.speed)

    if location != 'at the station':
        # update all packages status' to "en route" as truck has left the station
        for pkg in truck.packages:
            if pkg[8] != 'CANCELED':
                pkg[8] = 'en route'

        for i in range(len(truck.route) - 1):

            # calculate the miles between the current address and the next address on the route using graphs edge's
            miles = distances[truck.route[i], truck.route[i + 1]]
            minutes = miles / truck.speed       # calculate the minutes based on trucks speed.
            time_of_delivery = (truck.time + timedelta(minutes=minutes))       # add the minutes to the current trucks time to get delivery time
            truck.time = time_of_delivery

            # if the estimated time of delivery is less than the user requested time_stamp, the truck is allowed to proceed.
            # miles are accumulated, the packages status is updated, a new next package and next est arrival are updated.

            if time_of_delivery.time() < time_stamp.time():
                truck.miles_traveled += miles
                status = 'delivered at {}'.format(str(time_of_delivery.time()))
                for pkg in truck.packages:
                    return_check = truck.route[i + 1]
                    if truck.route[i + 1] == pkg[1] and pkg[8] != 'CANCELED':
                        # update the package status from en route to time of delivery
                        pkg[8] = status
                        # saves the next package information on the list to later display which package is currently in progress and eta
                        next_address = truck.route[i + 2]
                        next_est_arrival = truck.time + timedelta(minutes= distances[truck.route[i + 1], truck.route[i + 2]] / truck.speed)

    # pretty print truck information
    print("{} {}.".format(truck.name, location))
    truck.print_truck_packages_info(next_address, next_est_arrival)

    # No more packages are "en route" status, set the trucks finish time. This will let truck 3 know when to leave.
    if 0 == len([pkg for pkg in truck.packages if pkg[8] == 'en route' or pkg[8] == 'at station']):
        if return_check == '4001 S 700 E':
            truck.finish = truck.time
            print('**** {} returned to the station at {} ****'.format(truck.name, truck.finish.time()))
        else:
            print('**** Truck is on its way back to the station ****')
    else:
        truck.finish = datetime(2020, 10, 20, 17, 0, 0)

    print()

# search for an individual package at the current time and print package information neatly
def search_package(id):
    pkg = pkg_hash.find_pkg(id)
    if pkg != None:
        print('Package ID: {}\n'
              'Delivery Address: {}\n'
              'Weight: {}\n'
              'Deadline: {}\n'
              'Special Notes: {}\n'
              'Currently on {}\n'
              'Status: {}\n'.format(pkg[0], ' '.join(pkg[1:5]), pkg[6], pkg[5], ('None' if pkg[7] == '' else pkg[7]), pkg[-1], pkg[8]))

def update_package(updated_pkg):
    # need to update a particular package. first search for the package by id. if the search returns a match, we replace
    # the package with the updated package
    id = updated_pkg[0]
    pkg = pkg_hash.find_pkg(id)
    updated_pkg.extend([pkg[8], pkg[-1]])
    pkg_hash.update_pkg(updated_pkg)
    truck = trucks[pkg[-1]]
    truck.packages[truck.packages.index(pkg)] = updated_pkg
    truck.reset()

# remove a package from a truck if it's still at the station, cancel it if it hasn't been delivered O(N)
def remove_package(id):
    pkg = pkg_hash.find_pkg(id)
    if pkg != None:

        # each package was appended the truck name when it was placed onto the truck. therefore, we can obtain the appropriate truck.
        truck = trucks[pkg[-1]]
        # the truck w/ the package becomes "truck_match". we remove the package from the truck with the remove_pkg function of the truck class.
        if pkg[8] == 'delayed' or pkg[8] == 'at station':
            # one last check to see if user is sure about package removal
            verify = input(
                'The package is on {} which is currently {}. Are you sure you want to remove it?  (y or n)  --->  '.format(pkg[-1], pkg[8]))
            if 'y' in verify.lower():
                truck.remove_pkg(pkg)
                pkg_hash.remove_pkg(id)
            else:
                print('package removal canceled.')

        # if package status is delivered, package can no longer be canceled or removed.
        elif 'delivered' in pkg[8]:
            print('The package is on {} and was already {}. Can no longer cancel.'.format(pkg[-1], pkg[8]))

        # Package has already left the station but user can still cancel it and reroute.
        else:
            print('The package is on {} which is currently {}. Package delivery will be canceled.'.format(pkg[-1], pkg[8]))
            truck.cancel_pkg(pkg)




# obtain the hash map for easy search
pkg_hash = prepare_packages("Packages.csv")

# Create the graph
graph = prepare_distance_graph("Distances.csv", pkg_hash)

# create 3 truck classes with unique names
truck1 = truck('truck 1')
truck2 = truck('truck 2')
truck3 = truck('truck 3')
# create helper dictionary to locate a particular truck by name
trucks = {truck1.name: truck1, truck2.name: truck2, truck3.name: truck3}
# load the trucks
load_trucks()

# find the best route
get_routes()
