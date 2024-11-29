import datetime

class Package:
    def __init__(self, pckg_id, address, city, state, zip_code, 
                 deadline, weight, status = "At Hub", truck_loaded_to = -1):
        self.id = pckg_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = datetime.time()
        self.truck_loaded_to = truck_loaded_to