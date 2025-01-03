from ..extensions import db


class Addresses(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), nullable=True)
    district = db.Column(db.String(20))
    street = db.Column(db.String(20))
    house = db.Column(db.String(10))
    entrance = db.Column(db.Integer, db.CheckConstraint("entrance > 0 or entrance is null"), nullable=True)
    floor = db.Column(db.Integer, db.CheckConstraint("floor BETWEEN 0 AND 50 or floor is null"), nullable=True)
    flat = db.Column(db.Integer, db.CheckConstraint("flat > 0 or flat is null"), nullable=True)



    def __init__(self, city=True, district=None, street=None, house=None, entrance=None, floor=None, flat=None):
        self.city = city
        self.district = district
        self.street = street
        self.house = house
        self.entrance = entrance
        self.floor = floor
        self.flat = flat