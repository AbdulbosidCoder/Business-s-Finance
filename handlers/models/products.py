import datetime


class Product:
    def __init__(self, id=None, product_code="", description="", created_by=None,
                 created=datetime.date.today(), price=0.0, quantity=0):
        self.product_telegram_id = None
        self.id = id
        self.product_code = product_code
        self.description = description
        self.created_by = created_by
        self.created = created
        self.price = price
        self.quantity = quantity
        self.photo_list = []

    @classmethod
    def from_tuple(cls, attribute_tuple):
        return cls(*attribute_tuple)

    @classmethod
    def from_dict(cls, attribute_dict):
        return cls(**attribute_dict)

    def save(self,database):
        database.create_product(self)
        return print("Product saved")


