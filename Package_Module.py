class Package:
    def __init__(self, address, deadline, city, zip_code, weight, status, delivery_time=None):
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time