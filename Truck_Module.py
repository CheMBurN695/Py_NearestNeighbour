class Truck:
    def __init__(self, truck_ID, packages=None, currentAddress="4001 South 700 East",
                 mileage=0, time_departed=0, time_In_Transit= 0):
        self.truck_ID = truck_ID
        self.packages = packages if packages is not None else []
        self.currentAddress = currentAddress
        self.mileage = mileage
        self.time_departed = time_departed
        self.time_In_Transit = time_In_Transit

    def __str__(self):
        return (f"Truck ID: {self.truck_ID}, Packages: {len(self.packages)}, "
                f"Current Address: {self.currentAddress}, Mileage: {self.mileage}, "
                f"Time Departed: {self.time_departed}, Time In Transit: {self.timeInTransit}")
