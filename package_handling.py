# Matthew Leyden
# Student ID: 001008459
# Data Structures and Algorithms 2

import csv

class Graph:

    # address list to keep track of addresses, vertices dictionary where we will place which packages will go to
    # which addresses, and edge dictionary that will hold the miles between each address
    def __init__(self):
        self.num_packages = 0
        self.address_list = []
        self.vertices = {}
        self.edges = {}

    # an edge weight between 2 locations O(1)
    def edge(self, vertex1, vertex2, miles):
        self.edges[(vertex1, vertex2)] = miles


    def vertex(self, vertex):
        self.vertices[vertex] = []
        self.address_list.append(vertex)


    # put packages from the hash map into the vertices dictionary address key to which it belongs. (N^2)
    def place_packages(self, pkg_hash):
        for bucket in pkg_hash.map:
            for pkg in bucket:
                self.num_packages +=1
                self.vertices[pkg[1]].append(pkg)


class HashMap:

    # constructor for hash map
    def __init__(self):
        self.map = [[], [], [], [], [], [], [], [], [], []]
        self.num_packages = 0

    # hash function O(1)
    def hash(self, id):
        bucket_number = int(id) % len(self.map)
        bucket = self.map[bucket_number]
        return bucket, bucket_number

    # find a package in hash map (if exists) using id
    def find_pkg(self, id):
        bucket, num = self.hash(id)
        for pkg in bucket:
            if pkg[0] == id:
                return pkg  # package located
        print('package not found.')



    # insert a package in the hash map by unique id  O(1)
    def insert_pkg(self, pkg):
        id = int(pkg[0])
        bucket = id % len(self.map)
        self.map[bucket].append(pkg)
        self.num_packages +=1


    # update a package by using self.hash to obtain the bucket and bucket number. If the package is found by id, it is
    # replaced with the updated package. O(N)
    def update_pkg(self, updated_package):
        bucket, num = self.hash(updated_package[0])
        find_old_package = [c for c in bucket if c[0] == updated_package[0]]
        if find_old_package != []:
            bucket[bucket.index(find_old_package[0])] = updated_package
            self.map[num] = bucket

        else:
            print('package not found')

    # remove a package from the hash map  O(N)
    def remove_pkg(self, id):
        bucket, num = self.hash(id)
        pkg = [c for c in bucket if c[0] == id]
        if pkg != []:
            self.map[num] = [c for c in bucket if c[0] != id]
            print('package successfully removed')
        else:
            print('package not found')


# takes the Packages csv and implements a hash map (pkg_hash) for easy search.
def prepare_packages(file1):
    pkg_hash = HashMap()
    with open(file1) as f:
        reader = csv.reader(f)
        next(reader)
        for item in reader:
            pkg_hash.insert_pkg(item)

    return pkg_hash

def prepare_distance_graph(file2, pkg_hash):
    # opens the Distances csv and creates a graph from distance data of each address to every other address.
    # key = (address1, address2), value = miles between  O(N^2)
    distance_graph = Graph()
    distance_list = []
    with open(file2) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            distance_graph.vertex(row[1])
            distance_list.append(row)
    for row in distance_list:
        for i in range(3, len(row)):
            distance_graph.edge(row[1], distance_list[i - 3][1], float(row[i]))

    distance_graph.place_packages(pkg_hash)
    return distance_graph

