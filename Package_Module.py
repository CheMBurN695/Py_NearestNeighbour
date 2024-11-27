class Package:
    def __init__(self, pckg_id, address, deadline, city, zip_code, weight, status = None, delivery_time=None):
        self.id = pckg_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time