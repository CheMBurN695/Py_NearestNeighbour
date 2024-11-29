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

# load all packages from CSV file
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

# load address data from CSV file
def load_address_data():
    with open("CSV Files/addressCSV.csv") as addressCSV:
        reader = csv.reader(addressCSV)
        for row in reader:
            addressData.append(str.strip(row[2]))
       
# load distance data from CSV file
def load_distance_data():
    with open("CSV Files/distanceCSV.csv") as distanceCSV:
        reader = csv.reader(distanceCSV, delimiter=',')
        count = 0
        for row in reader:
            distList = [float(x) for x in row[0 : count + 1]]
            distanceData.append(distList)
            count += 1

# package lookup from the hashmap   
def get_package(_pckgID):
    pckgID = str(_pckgID)
    package = packageHashMap.get(pckgID)
    if package is None:
        print(f"Warning: Package ID {pckgID} not found in HashMap.")
    return package

# get a list of packages from a list of package IDs
def get_package_list(pckgIDList):
    packageList = []
    for pckgID in pckgIDList:
        packageList.append(get_package(pckgID))
    return packageList

# get the distance between two addresses
def get_distance(address1, address2):
    index1 = addressData.index(address1)
    index2 = addressData.index(address2)
    if index1 >= len(distanceData) or index2 >= len(distanceData[index1]):
        return distanceData[index2][index1]
    else:
        return distanceData[index1][index2]

# create trucks and set their departure times
def create_trucks():
    for i in range(truckCount):
        trucks.append(Truck(i + 1))
        trucks[i].time_In_Transit = datetime.timedelta()
    trucks[0].time_departed = datetime.timedelta(hours=8)
    trucks[1].time_departed = datetime.timedelta(hours=9, minutes=5)
    trucks[2].time_departed = datetime.timedelta(hours=10, minutes=20)        

# get the package closest to a given address
def get_package_closest_to_address(address):
    min_distance = 20000
    nearest_package = None
    for package in all_package_list:
        distance = get_distance(address, package.address)
        if (distance < min_distance):
            min_distance = distance
            nearest_package = package
    return nearest_package

# get the package closest to a given address from a list of packages
def get_package_closest_to_address_custom(address, package_list):
    min_distance = 20000
    nearest_package = None
    for package in package_list:
        distance = get_distance(address, package.address)
        if (distance < min_distance):
            min_distance = distance
            nearest_package = package
    return nearest_package

# load trucks optimally
def load_trucks_optimally():
    all_packages = list(all_package_list)
    
    # load static packages based on requirements
    for truck in trucks:
        
        if truck.truck_ID == 1:
            packages_for_truck_1_ids = [13, 15, 19, 1, 20, 16, 29, 30, 31, 34, 37, 40]
            packages_for_truck1 = get_package_list(packages_for_truck_1_ids)
            truck.packages.extend(packages_for_truck1)

            # remove the packages that are already loaded to the truck
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
            packages_for_truck_3_ids = [25, 28, 32, 39, 35, 33, 27, 26, 23, 11, 9]
            packages_for_truck3 = get_package_list(packages_for_truck_3_ids)
            truck.packages.extend(packages_for_truck3)
            for pkg in reversed(all_packages):
                if (packages_for_truck3.__contains__(pkg)):
                    all_packages.remove(pkg)

    # load remaining packages
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

    # set truck_loaded_to for each package
    for truck in trucks:
        for package in truck.packages:
            package.truck_loaded_to = truck.truck_ID


# manage truck delivery
def manage_truck_delivery():
    do_delivery(trucks[0])
    do_delivery(trucks[1])

    #get least travelled truck
    truckFirstDone = None
    if (trucks[0].time_In_Transit > trucks[1].time_In_Transit):
        truckFirstDone = trucks[1]
    else:
        truckFirstDone = trucks[0]

    #get the distance back to the hub and add it to the mileage + travel time
    distanceBackToHub = get_distance(truckFirstDone.currentAddress, addressData[0])
    truckFirstDone.mileage += distanceBackToHub
    truckFirstDone.time_In_Transit += datetime.timedelta(minutes=(distanceBackToHub / 18) * 60)

    #at this point the driver switches

    do_delivery(trucks[2])

# deliver packages using on nearest neighbour algorithm
def do_delivery(truck):
    truck.mileage = 0
    current_elapsed_time = truck.time_departed

    for package in truck.packages:
        package.status = "En Route"

    #split between priorities and non-priorities to ensure deadlines are met
    priority_packages = [package for package in truck.packages if package.deadline == "9:00 AM"]
    if (truck.truck_ID == 2):   # truck that leaves at 9:05 AM has a different priority
        priority_packages = [package for package in truck.packages if package.deadline == "9:00 AM" or package.deadline == "10:30 AM"]         
    other_packages = [package for package in truck.packages if package.deadline != "9:00 AM"]
    truck.packages = priority_packages + other_packages

    # Deliver all priority packages
    while (len(priority_packages) > 0):
        min_distance = 20000  # Initialize with a high value to find the nearest package
        nearest_package = None
        for package in priority_packages:
            distance = get_distance(truck.currentAddress, package.address)  # Calculate distance to each priority package
            if (distance < min_distance):  # Check if this package is closer
                min_distance = distance
                nearest_package = package

        truck.mileage += min_distance  # Add the distance to the truck's total mileage
        truck.currentAddress = nearest_package.address  # Update the truck's current location
        priority_packages.remove(nearest_package)  # Remove the delivered package from the priority list
        truck.time_In_Transit += datetime.timedelta(minutes=(min_distance / 18) * 60)  # Update the time in transit
        current_elapsed_time += truck.time_In_Transit  # Update the elapsed delivery time
        
        nearest_package.status = "Delivered"  # Mark the package as delivered
        nearest_package.delivery_time = truck.time_In_Transit + truck.time_departed  # Record the delivery time

    # Deliver all non-priority packages
    while (len(other_packages) > 0):
        min_distance = 20000
        nearest_package = None
        for package in other_packages:
            distance = get_distance(truck.currentAddress, package.address)
            if (distance < min_distance):
                min_distance = distance
                nearest_package = package

        truck.mileage += min_distance
        truck.currentAddress = nearest_package.address
        other_packages.remove(nearest_package)
        truck.time_In_Transit += datetime.timedelta(minutes=(min_distance / 18) * 60)
        current_elapsed_time += truck.time_In_Transit
        
        nearest_package.status = "Delivered" 
        nearest_package.delivery_time = truck.time_In_Transit + truck.time_departed

# Helper function to get the package status at a specific time
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

# Helper function to check if a package's deadline has been breached
def get_package_deadline_breached(package_id, current_time):
    nine_deadline = datetime.timedelta(hours=9)
    ten_deadline = datetime.timedelta(hours=10, minutes=30)
    package = get_package(package_id)
    
    if package is None:
        print(f"Package ID {package_id} not found.")
        return None

    if package.deadline == "10:30 AM":
        deadline = ten_deadline
    elif package.deadline == "9:00 AM":
        deadline = nine_deadline
    else:
        return False

    # If the current time is earlier than the deadline, it is not breached
    if current_time < deadline:
        return False

    # Otherwise, check if the package's delivery time exceeds the deadline
    if package.delivery_time > deadline:
        return True
    else:
        return False



# User Interface to view package status at a specific time
def run_UI():
    while True:
        print("\n--- WGUPS Package Delivery System ---")
        print("1. View total mileage of all trucks")
        print("2. View package status at a specific time")
        print("Enter 'exit' to quit the program.")

        user_option = input("\nEnter your choice (1 or 2): ").strip()
        if user_option.lower() == 'exit':
            print("Exiting the program.")
            break

        if user_option == "1":
            total_mileage = sum(truck.mileage for truck in trucks)
            print(f"\nTotal Mileage of All Trucks: {total_mileage:.2f} miles")
        
        elif user_option == "2":
            user_time_input = input("Enter the time (HH:MM): ").strip()
            if user_time_input.lower() == 'exit':
                print("Exiting the program.")
                break
            try:
                user_time = datetime.datetime.strptime(user_time_input, "%H:%M")
            except ValueError:
                print("Invalid time format. Please try again.")
                continue

            usertime_delta = datetime.timedelta(hours=user_time.hour, minutes=user_time.minute)

            for truck in trucks:
                print(f"\nTruck {truck.truck_ID}:")
                for package in all_package_list:
                    if package.truck_loaded_to == truck.truck_ID:
                        delivery_time = package.delivery_time
                        package_status = get_package_status_at_time(package.id, usertime_delta)
                        if usertime_delta < delivery_time:
                            delivery_time = "Pending delivery"
                        print(f"Package ID: {package.id}, Address: {package.address}, Status: {package_status}, Delivered At: {delivery_time}, Deadline Breached: {get_package_deadline_breached(package.id, usertime_delta)}")
        else:
            print("Invalid choice. Please enter '1', '2', or 'exit'.")

# Main functions to run the program

load_all_packages()
load_address_data()
load_distance_data()
create_trucks()
load_trucks_optimally()
manage_truck_delivery()
run_UI()