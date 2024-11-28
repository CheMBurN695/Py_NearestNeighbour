# Student ID - 012279499
# Pasindu De Silva

import csv
import datetime
from HashTable import HashMap
from Truck_Module import Truck
from Package_Module import Package

packageHashMap = HashMap()
distanceData = []
addressData = []
truckCount = 3
driverCount = 2
maxPackageCount = 16
trucks = []

def load_all_packages():
    with open("CSV Files/packageCSV.csv") as packageCSV:
        package_reader = csv.reader(packageCSV)
        for row in package_reader:
            package_id = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            _package = Package(package_id, address, city, state, zip_code, deadline, weight)
            packageHashMap.add(package_id, _package)

def load_address_data():
    with open("CSV Files/addressCSV.csv") as addressCSV:
        reader = csv.reader(addressCSV)
        for row in reader:
            addressData.append(str.strip(row[2]))
            
def load_distance_data():
    with open("CSV Files/distanceCSV.csv") as distanceCSV:
        reader = csv.reader(distanceCSV, delimiter=',')
        count = 0
        for row in reader:
            distList = [float(x) for x in row[0 : count + 1]]
            distanceData.append(distList)
            count += 1

def get_package(pckgID):
    return packageHashMap.get(pckgID)

def get_package_list(pckgIDList):
    packageList = []
    for pckgID in pckgIDList:
        packageList.append(get_package(pckgID))
    return packageList

def get_distance(address1, address2):
    index1 = addressData.index(address1)
    index2 = addressData.index(address2)
    return distanceData[index1][index2]

def create_trucks():
    for i in range(truckCount):
        trucks.append(Truck(i + 1))

def load_trucks():
    for i in range(len(trucks)):
        if (trucks[i].truck_ID == 1):
            trucks[i].packages = get_package_list([1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40])
            trucks[i].time_departed = datetime.timedelta(hours=8)
        elif (trucks[i].truck_ID == 2):
             trucks[i].packages = get_package_list([3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39])
             trucks[i].time_departed = datetime.timedelta(hours=10, minutes=20)
        else:
            trucks[i].packages = get_package_list([2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33])
            trucks[i].time_departed = datetime.timedelta(hours=9, minutes=5)

        trucks[i].currentAddressIndex = 0
        trucks[i].mileage = 0

load_all_packages()
load_address_data()
load_distance_data()
create_trucks()
load_trucks()

def do_delivery(truck):
    packages_loaded = truck.packages
    for package in packages_loaded:
        package.status = "En Route"
    while (len(packages_loaded) > 0):
        min_distance = 20000
        nearest_package = None
        for package in packages_loaded:
            distance = get_distance(truck.currentAddressIndex, package.addreses)
            if (distance < min_distance):
                min_distance = distance
                nearest_package = package

    

print(get_distance("2300 Parkway Blvd", "1060 Dalton Ave S"))