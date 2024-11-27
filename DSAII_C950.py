# Student ID - 012279499
# Pasindu De Silva

import csv
import datetime
import HashTable
import Truck
from Package_Module import Package

class MainProgram:
    def GetAllPackages(self):
        packages = []
        
        with open("CSV Files/packageCSV") as packageCSV:
            package_reader = csv.reader(packageCSV)
            for row in package_reader:
                package_id, address, city, state, zip_code, deadline, weight, special_notes = row
                _package = Package(package_id, address, city, state, zip_code, deadline, weight, special_notes)
                packages.append(_package)

        return packages

main = MainProgram()
packages = main.GetAllPackages()
