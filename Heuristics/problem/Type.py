class Type(object):
    def __init__(self, d_city, cap, cost, id):
        self.d_city = d_city
        self.cap = cap
        self.cost = cost
        self.id = id

    def get_d_city(self):
        return self.d_city

    def get_capacity(self):
        return self.cap

    def get_cost(self):
        return self.cost

    def get_id(self):
        return self.id
