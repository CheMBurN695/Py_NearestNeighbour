# Student ID - 012279499
# Pasindu De Silva

import csv
import datetime
from HashTable import HashMap
import Truck
from Package_Module import Package

packageHashMap = HashMap()
packages = []
distanceData = []
addressData = []

def GetAllPackages():
        
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
            packages.append(_package)
            packageHashMap.add(package_id, _package)

    return packages

def GetPackage(self, pckgID):
    return self.packageHashMap.get(pckgID)

def LoadAddressData():
    with open("CSV Files/addressCSV.csv") as addressCSV:
        reader = csv.reader(addressCSV)
        for row in reader:
            addressData.append(row)
            
def LoadDistanceData():
    with open("CSV Files/distanceCSV.csv") as distanceCSV:
        reader = csv.reader(distanceCSV)
        distanceData
        for row in reader:
            distanceData.append(row)

def printDistData():
    for i in distanceData:
        print(i)

LoadAddressData()
print(len(addressData))