# Matthew Leyden
# Student ID: 001008459
# Data Structures and Algorithms 2

from datetime import timedelta, datetime
class truck:

    # initialize truck class with unique name, speed (18 mph / 60 = 0.3 mi/min), maximum payload an empty package list, an empty route list, a start
    # time, a finish time, a time (current, depending on its delivery process), miles traveled, and a time_delay which will update the
    # start time as needed if certain packages are delayed
    def __init__(self, name):
        self.name = name
        self.speed = 18 / 60
        self.max_payload = 16
        self.packages = []
        self.route = []
        self.start = datetime(2020, 10, 20, 8, 0, 0)
        self.finish = datetime(2020, 10, 20, 17, 0, 0)
        self.time = None
        self.miles_traveled = 0
        self.time_delay = datetime(2020, 10, 20, 8, 0, 0)

    # insert a package into the package list. index the address and place into the trucks route.
    def insert_pkg(self, pkg):
        truck_pkg = pkg
        truck_pkg.append('status')
        truck_pkg.append(self.name)
        self.packages.append(truck_pkg)
        if truck_pkg[1] not in self.route:
            self.route.append(truck_pkg[1])
            self.reset()


    # this function is used to display all of the current route information for a truck at a particular time in an
    # easy to read and understand display.
    def print_truck_packages_info(self, next_address = None, next_est_arrival=None):

        pkgs_info = {}
        for item in self.packages:
            if item[1] == next_address and item[8] == 'en route':
                pkgs_info[item[0]] = [' '.join(item[1:5]), item[5], item[8] + '     (eta {})'.format(str(next_est_arrival.time())), item[7]]
            else:
                pkgs_info[item[0]] = [' '.join(item[1:5]), item[5], item[8], item[7]]

        print("{:<8} {:<70} {:<10} {:<30} {:<70}".format('ID #', 'DELIVERY ADDRESS', 'DEADLINE', 'STATUS', 'SPECIAL NOTES'))
        for k, v in pkgs_info.items():
            address, deadline, status, notes = v
            print("{:<8} {:<70} {:<10} {:<30} {:<70}".format(k, address, deadline, status, notes))

    # packages are removed from the truck. if the package is a unique address, remove from route and find_greedy_route
    def remove_pkg(self, pkg):
        if len([item[1] for item in self.packages if item[1] == pkg[1]]) == 1:
            self.route.remove(pkg[1])
        self.packages.remove(pkg)

    def cancel_pkg(self, pkg):
        pkg_index = self.packages.index(pkg)
        pkg[8] = 'CANCELED'
        self.packages[pkg_index] = pkg
        if len([item[1] for item in self.packages if item[1] == pkg[1]]) == 1:
            self.route.remove(pkg[1])


    # used to update a packages address
    def update_pkg(self, pkg):

        find_old_package = [c for c in self.packages if c[0] == pkg[0]]
        print(find_old_package)
        if find_old_package != []:
            print([item[1] for item in self.packages if item[1] == find_old_package[0][1]])
            if len([item[1] for item in self.packages if item[1] == find_old_package[0][1]]) == 1:
                self.route.remove(find_old_package[0][1])
            self.packages[self.packages.index(find_old_package[0])] = pkg
            self.route.insert(1, pkg[1])

        else:
            print('package not found')

    # used to reset a trucks status, time and miles information O(N)
    def reset(self):
        for pkg in self.packages:
            if 'delayed' in pkg[7].lower():
                pkg[8] = "delayed"
            elif pkg[8] == 'CANCELED':
                pass
            else:
                pkg[8] = "at station"
        self.start = self.time_delay
        self.finish = datetime(2020, 10, 20, 17, 0, 0)
        self.time = None
        self.miles_traveled = 0
