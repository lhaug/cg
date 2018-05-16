import math

class Vektor(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)

    def pos(self):
        x = self.x
        y = self.y
        z = self.z
        if x < 0:
            x *= (-1)
        if y < 0:
            y *= (-1)
        if z < 0:
            z *= (-1)
        return Vektor(x, y, z)

    def __add__(self, other):
        a = self.x + other.x
        b = self.y + other.y
        c = self.z + other.z
        return Vektor(a, b, c)

    def __sub__(self, other):
        a = self.x - other.x
        b = self.y - other.y
        c = self.z - other.z
        return Vektor(a,b,c)

    def __mul__(self, other):
        a = self.x * other.x
        b = self.y * other.y
        c = self.z * other.z
        return Vektor(a, b, c)

    def __div__(self, other):
        a = self.x / other.x
        b = self.y / other.y
        c = self.z / other.z
        return Vektor(a, b, c)

    def div(self, p):
        a = self.x / p
        b = self.y / p
        c = self.z / p
        return Vektor(a, b, c)

    def normalized(self):
        length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return self.div(length)

    def cross(self, other):
        a = (self.y * other.z) - (self.z * other.y)
        b = (self.z * other.x) - (self.x * other.z)
        c = (self.x * other.y) - (self.y * other.x)
        return Vektor(a, b, c)

    def scale(self,t):
        a = self.x * t
        b = self.y * t
        c = self.z * t
        return Vektor(a, b, c)

    def dot(self,other):
        a = self.x * other.x
        b = self.y * other.y
        c = self.z * other.z
        return (a+b+c)

    def __lt__(self, other):
        if self.x < other.x and self.y < other.y:
            return True
        else:
            return False

    def __le__(self, other):
        if self.x <= other.x and self.y <= other.y:
            return True
        else:
            return False
    def __gt__(self, other):
        if self.x > other.x and self.y > other.y:
            return True
        else:
            return False
    def __ge__(self, other):
        if self.x >= other.x and self.y >= other.y:
            return True
        else:
            return False

    def point(self):
        a = self.x / self.z
        b = self.y / self.z
        c = self.z / self.z

        return Vektor(a, b, c)