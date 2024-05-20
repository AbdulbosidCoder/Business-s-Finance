from aiogram.fsm.state import StatesGroup, State


class ProductStates(StatesGroup):
    change_str_attributes = State()
    change_int_attributes = State()
    get_product_code_to_change = State()
    change_attributes = State()
    added_product = State()
    add_product = State()
    sold_product = State()
    sell_product = State()
    detele_product = State()
    product_description = State()
    product_price = State()
    product_quantity = State()
    product_code = State()
    product_photo = State()
