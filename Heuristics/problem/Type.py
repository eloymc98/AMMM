class Type(object):
    def __init__(self, d_city, cap, cost):
        self.d_city = d_city
        self.cap = cap
        self.cost = cost

    def get_d_city(self):
        return self.d_city

    def get_capacity(self):
        return self.cap

    def get_cost(self):
        return self.cost
