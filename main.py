# Student ID - 012279499
# Pasindu De Silva

import csv
import datetime
from HashTable import HashMap
from Truck_Module import Truck
from Package_Module import Package

packageHashMap = HashMap()
all_package_list = []
distanceData = []
addressData = []
truckCount = 3
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
            _package.status = "At Hub"
            packageHashMap.add(package_id, _package)        
            all_package_list.append(_package)

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

def get_package(_pckgID):
    pckgID = str(_pckgID)
    package = packageHashMap.get(pckgID)
    if package is None:
        print(f"Warning: Package ID {pckgID} not found in HashMap.")
    return package

def get_package_list(pckgIDList):
    packageList = []
    for pckgID in pckgIDList:
        packageList.append(get_package(pckgID))
    return packageList

def get_distance(address1, address2):
    index1 = addressData.index(address1)
    index2 = addressData.index(address2)
    if index1 >= len(distanceData) or index2 >= len(distanceData[index1]):
        return distanceData[index2][index1]
    else:
        return distanceData[index1][index2]

def create_trucks():
    for i in range(truckCount):
        trucks.append(Truck(i + 1))
        trucks[i].time_In_Transit = datetime.timedelta()
    trucks[0].time_departed = datetime.timedelta(hours=8)
    trucks[1].time_departed = datetime.timedelta(hours=9, minutes=5)
    trucks[2].time_departed = datetime.timedelta(hours=10, minutes=20)        

def get_package_closest_to_address(address):
    min_distance = 20000
    nearest_package = None
    for package in all_package_list:
        distance = get_distance(address, package.address)
        if (distance < min_distance):
            min_distance = distance
            nearest_package = package
    return nearest_package

def get_package_closest_to_address_custom(address, package_list):
    min_distance = 20000
    nearest_package = None
    for package in package_list:
        distance = get_distance(address, package.address)
        if (distance < min_distance):
            min_distance = distance
            nearest_package = package
    return nearest_package

def load_trucks_optimally():
    all_packages = list(all_package_list)

    # load statics
    for truck in trucks:
        
        if truck.truck_ID == 1:
            packages_for_truck_1_ids = [13, 15, 19, 1, 20, 16, 29, 30, 31, 34, 37, 40]
            packages_for_truck1 = get_package_list(packages_for_truck_1_ids)
            truck.packages.extend(packages_for_truck1)
            for pkg in reversed(all_packages):
                if (packages_for_truck1.__contains__(pkg)):
                    all_packages.remove(pkg)

        if truck.truck_ID == 2:
            packages_for_truck_2_ids = [3, 18, 36, 38]
            packages_for_truck2 = get_package_list(packages_for_truck_2_ids)
            truck.packages.extend(packages_for_truck2)            
            for pkg in reversed(all_packages):
                if (packages_for_truck2.__contains__(pkg)):
                    all_packages.remove(pkg)

        if truck.truck_ID == 3:
            packages_for_truck_3_ids = [6, 25, 28, 32, 39, 35, 33, 27, 26, 23, 11, 9]
            packages_for_truck3 = get_package_list(packages_for_truck_3_ids)
            truck.packages.extend(packages_for_truck3)
            for pkg in reversed(all_packages):
                if (packages_for_truck3.__contains__(pkg)):
                    all_packages.remove(pkg)

    for truck in trucks:
        # only get from packages in truck to find the starting package
        package_closest_to_hub = get_package_closest_to_address_custom(truck.currentAddress, truck.packages)
        current_package = package_closest_to_hub
        while (len(truck.packages) < 16 and len(all_packages) > 0):
            if (current_package is None):
                break
            next_package = get_package_closest_to_address_custom(current_package.address, all_packages)
            truck.packages.append(next_package)
            all_packages.remove(next_package)
            current_package = next_package

    for truck in trucks:
        for package in truck.packages:
            package.truck_loaded_to = truck.truck_ID


def manage_truck_delivery():
    do_delivery(trucks[0])
    do_delivery(trucks[1])

    #get least travelled truck
    truckFirstDone = None
    if (trucks[0].time_In_Transit > trucks[1].time_In_Transit):
        truckFirstDone = trucks[1]
    else:
        truckFirstDone = trucks[0]

    distanceBackToHub = get_distance(truckFirstDone.currentAddress, addressData[0])
    truckFirstDone.mileage += distanceBackToHub
    truckFirstDone.time_In_Transit += datetime.timedelta(minutes=(distanceBackToHub / 18) * 60)

    #at this point the driver switches

    do_delivery(trucks[2])

def do_delivery(truck):
    truck.mileage = 0
    for package in truck.packages:
        package.status = "En Route"
    while (len(truck.packages) > 0):
        min_distance = 20000
        nearest_package = None
        for package in truck.packages:
            distance = get_distance(truck.currentAddress, package.address)
            if (distance < min_distance):
                min_distance = distance
                nearest_package = package

        truck.mileage += min_distance
        truck.currentAddress = nearest_package.address
        truck.packages.remove(nearest_package)
        truck.time_In_Transit += datetime.timedelta(minutes=(min_distance / 18) * 60)
        
        nearest_package.status = "Delivered"
        nearest_package.delivery_time = truck.time_In_Transit + truck.time_departed

def get_package_status_at_time(package_id, current_time):
    package = get_package(package_id)
    if package is None:
        return None
    if (current_time < trucks[package.truck_loaded_to -1].time_departed):
        return "At Hub"
    if (package.delivery_time != datetime.timedelta(0)):
        if (package.delivery_time <= current_time):
            return "Delivered"
        else:
            return "En Route"

def get_package_deadline_breached(package_id):
    nine_deadline = datetime.timedelta(hours=9)
    ten_deadline = datetime.timedelta(hours=10, minutes=30)
    package = get_package(package_id)
    if package is None:
        #display error
        return None
    if (package.deadline == "10:30 AM" and package.delivery_time > ten_deadline):
        return True
    elif (package.deadline == "9:00 AM" and package.delivery_time > nine_deadline):
        return True
    else:
        return False


def run_UI():

    print("\n--- WGUPS Package Delivery System ---")
    print("View package status at a specific time.")

    user_time_input = input("Enter the time (HH:MM): ")
    try:
        user_time = datetime.datetime.strptime(user_time_input, "%H:%M")
    except ValueError:
        print("Invalid time format. Please try again.")
        return

    usertime_delta = datetime.timedelta(hours=user_time.hour, minutes=user_time.minute)

    total_mileage = 0
    for truck in trucks:
        print(f"\nTruck {truck.truck_ID}:")
        for package in all_package_list:
            if (package.truck_loaded_to == truck.truck_ID):
                delivery_time = package.delivery_time
                package_status = get_package_status_at_time(package.id, usertime_delta)
                print(f"Package ID: {package.id}, Address: {package.address}, Status: {package_status}, Deadline: {package.deadline}, Deadline Breached: {get_package_deadline_breached(package.id)}")
        total_mileage += truck.mileage

    print(f"\nTotal Mileage of All Trucks: {total_mileage:.2f} miles")

load_all_packages()
load_address_data()
load_distance_data()
create_trucks()
load_trucks_optimally()
manage_truck_delivery()
run_UI()