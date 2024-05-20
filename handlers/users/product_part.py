import uuid
import datetime
import os
from aiogram import types, F
from aiogram.methods import SendPhoto
from aiogram.types import Message, FSInputFile, KeyboardButton
from loader import db, dp, bot
from aiogram.fsm.context import FSMContext
from handlers.models.products import Product
from states.product_states import ProductStates
from utils.creater_menu.creater import create_menu
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup
from keyboards.default.user_buttons.users_button import users_button
users = {}
products = {}


class Market:
    data = {}
    take = 9
    skip = 0

    def __init__(self):
        self.change_product = None
        self.attribute = None
        self.added_product = None
        self.sold_product = None

    def add_product(self, product: Product):
        self.data[product.product_code] = product

    @staticmethod
    def save():
        if Market.data:
            for i in Market.data.values():
                db.create_product(i)
        Market.data.clear()
        return True


def get_user(telegram_id: str) -> Market:
    try:
        user = users[telegram_id]
    except:
        users[telegram_id] = Market
        user = users[telegram_id]

    return user


def get_product(telegram_id: str) -> Product:
    try:
        product = products[telegram_id]
    except:
        products[telegram_id] = Product()
        product = products[telegram_id]
    return product


"""GET"""


@dp.message(F.text == "Get product info")
async def get_products_info(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    await message.answer("Please wait !")
    titles = create_menu(take=user.take, skip=user.skip, database=db)

    menu_button = InlineKeyboardBuilder()
    menu_button.row(InlineKeyboardButton(text="<-previous", callback_data="previous_get_products_info"),
                    InlineKeyboardButton(text="next->", callback_data="next_get_products_info"))
    photo = FSInputFile("media/menu_of_products/menu.jpg")
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=photo,
                         caption="Menu",
                         reply_markup=menu_button.as_markup())

    titles_button = []
    for i in titles:
        titles_button.append([KeyboardButton(text=i)])
    title_ = ReplyKeyboardMarkup(keyboard=titles_button,
                                 resize_keyboard=True
                                 )
    await bot.send_message(chat_id=message.from_user.id, text="Please enter the product code : ", reply_markup=title_)
    await state.set_state(ProductStates.product_code)


@dp.callback_query(F.data.startswith(("next", "previous")))
async def movement(callback_data: types.CallbackQuery, state: FSMContext):
    user = get_user(str(callback_data.from_user.id))
    products = db.get_all_products()
    if callback_data.data.startswith("next"):
        move = callback_data.data.split("next_")
        user.skip += 9
        if user.skip > len(products):
            user.skip = len(products) - 9
        await globals()[move[1]](callback_data, state)
    else:
        move = callback_data.data.split("previous_")
        user.skip -= 9
        if user.skip < 0:
            user.skip = 0
        await globals()[move[1]](callback_data, state)




@dp.message(ProductStates.product_code)
async def find_product_by_code(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    user.take = 9
    user.skip = 0
    product = db.get_product_by_product_code(message.text)
    if product is None:
        await message.answer("Product not found "
                             "\nPlease resend the product code : ")
    else:
        product_ = Product(*product)
        photo = db.get_photo_by_product_id(product[0])
        for i in photo:
            await message.answer_photo(FSInputFile(i[2]))
        await message.answer_photo(FSInputFile(i[2]),
                                   caption=f"Product Code : {product_.product_code}\n Price : {product_.price}\n Quantity : {product_.quantity},\nTotal Price: {product_.price * product_.quantity}", reply_markup=users_button)
    await state.clear()


"""CREATE"""


@dp.message(F.text == "Create Product")  # Create New Product
async def create_product_main(message: types.Message, state: FSMContext):
    await message.answer("Please send the product photo: (360x240)")
    await state.set_state(ProductStates.product_photo)


@dp.message(ProductStates.product_photo)
async def get_product_photo(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    product = get_product(telegram_id=str(message.from_user.id))
    try:
        photo = message.photo[-1].file_id
        product.product_code = generate_short_uuid()
        photo_name = generate_short_uuid()
        product.product_telegram_id = photo
        photo = await bot.download(file=photo,
                                   destination=f"media/product/{photo_name}.jpg",
                                   timeout=1)
        product.photo_list.append(f"media/product/{photo_name}.jpg")
        product.photo_url = photo
        # Save the photo
        # with open(f"D:\\PycharmProjects\\Finance\\media\\product\\{product.product_code}.jpg", 'wb') as file:
        #     await photo_file.download(out=file)
        await state.set_state(ProductStates.product_price)
    except IndexError or AttributeError or KeyError:
        await message.answer("Please send me picture")
        return

    await message.answer("Enter product price:")


@dp.message(ProductStates.product_price)
async def get_product_price(message: types.Message, state: FSMContext):
    product = get_product(str(message.from_user.id))
    try:
        product.price = float(message.text)
        await message.answer("Please send product quantity:")
        await state.set_state(ProductStates.product_quantity)
    except:
        await message.answer("Please send product price without any extra charters")
        return


@dp.message(ProductStates.product_quantity)
async def get_product_quantity(message: types.Message, state: FSMContext):
    product = get_product(str(message.from_user.id))
    try:
        product.quantity = int(message.text)
        await message.answer("Write description.")
        await state.set_state(ProductStates.product_description)
    except:
        await message.answer("Please enter product quantity without any extra characters")
        return


@dp.message(ProductStates.product_description)
async def get_product_description(message: types.Message, state: FSMContext):
    product = get_product(str(message.from_user.id))
    product.description = str(message.text)
    product.created = datetime.date.today()
    product.created_by = db.get_user_by_telegra_id(message.from_user.id)[0]
    product.save(db)
    product_id = db.get_product_by_product_code(product.product_code)
    for i in product.photo_list:
        db.connect_photo_with_product(product_id=product_id[0], photo=i)
    product.photo_list.clear()
    await state.clear()
    await bot.send_photo(chat_id=message.from_user.id, photo=FSInputFile(i))
    await message.answer("Product is successfully created",reply_markup=users_button)


def generate_short_uuid():
    short_uuid = str(uuid.uuid4())[:8]
    return short_uuid


"""DELETE"""


@dp.message(F.text == "Delete Product")
async def delete_product(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    await message.answer("Please wait !")
    titles = create_menu(take=user.take, skip=user.skip, database=db)
    menu_button = InlineKeyboardBuilder()
    menu_button.row(InlineKeyboardButton(text="<-previous", callback_data="previous_delete_product"),
                    InlineKeyboardButton(text="next->", callback_data="next_delete_product"))
    menu = FSInputFile("media/menu_of_products/menu.jpg")
    await bot.send_photo(chat_id=message.from_user.id, photo=menu,
                         reply_markup=menu_button.as_markup())
    titles_button = []
    for i in titles:
        titles_button.append([KeyboardButton(text=i)])
    title_ = ReplyKeyboardMarkup(keyboard=titles_button,
                                 resize_keyboard=True
                                 )
    await bot.send_message(chat_id=message.from_user.id, text="Select product to delete", reply_markup=title_)
    await state.set_state(ProductStates.detele_product)


@dp.message(ProductStates.detele_product)
async def delete_product_continue(message: types.Message, state: FSMContext):
    product = db.get_product_by_product_code(message.text)
    if product is None:
        await message.answer("Product not found, Please enter product code")
    else:
        photos = db.get_photo_by_product_id(product[0])
        if product[6] == 0:
            db.delete_product_by_product_code(message.text)
        else:
            creater = db.get_user_by_telegra_id(message.from_user.id)
            db.note_outgoing_payment(message.from_user.id, product[1], product[6] * product[5], creater[0],
                                     created_at=datetime.datetime.today())
        for i in photos:
            os.remove(i[-1])
            # for analits
            # outgoing payment
        await message.answer("Product successfully deleted", reply_markup=users_button)


"""SELLING"""


@dp.message(F.text == "Sell Product")
async def sell_product(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    await message.answer("Please wait !")
    titles = create_menu(take=user.take, skip=user.skip, database=db)
    menu_button = InlineKeyboardBuilder()
    menu_button.row(InlineKeyboardButton(text="<-previous", callback_data="previous_sell_product"),
                    InlineKeyboardButton(text="next->", callback_data="next_sell_product"))
    menu = FSInputFile("media/menu_of_products/menu.jpg")
    titles_button = []

    for i in titles:
        titles_button.append([KeyboardButton(text=i)])

    title_ = ReplyKeyboardMarkup(keyboard=titles_button,
                                 resize_keyboard=True
                                 )
    await bot.send_photo(chat_id=message.from_user.id, photo=menu,
                         reply_markup=menu_button.as_markup())
    await bot.send_message(chat_id=message.from_user.id, text="Select product which you sold", reply_markup=title_, parse_mode="HTML")
    await state.set_state(ProductStates.sell_product)


@dp.message(ProductStates.sell_product)
async def sell_product_continue_part_1(message: types.Message, state: FSMContext):
    users = get_user(str(message.from_user.id))
    product = db.get_product_by_product_code(message.text)
    if product is None:
        await message.answer("Product does not exist\nPlease enter product code")
    else:
        user = db.get_user_by_id(product[3])
        user_market = users
        user_market.sold_product = product[1]
        product_photo = db.get_photo_by_product_id(product[0])
        for i in product_photo:
            await message.answer_photo(FSInputFile(i[2]))

        await message.answer_photo(FSInputFile(i[2]),
                                   caption=f"Product Code: {product[1]},\nProduct Description: {product[3]},\nCreated By: {user[1]},\nCreate at: {product[4]}\nPrice: {product[5]}, \nQuantity: {product[6]}")
        await message.answer("Please enter How many do you want to sell the product: ")
        await state.set_state(ProductStates.sold_product)


@dp.message(ProductStates.sold_product)
async def sell_product_continue_part_2(message: types.Message, state: FSMContext):
    try:
        sold = int(message.text)
        user = get_user(str(message.from_user.id))
        product = db.get_product_by_product_code(user.sold_product)
    except Exception as e:
        print(e)
        await message.answer("Please enter product code without any extra charters.")
        return
    if int(product[6]) > sold:
        quantity = int(product[6]) - sold
        user_data = db.get_user_by_telegra_id(message.from_user.id)
        db.note_incoming_payment(user_telegram_id=message.from_user.id, product_title=product[1],
                                 menturement=sold * int(product[5]), created_by=user_data[0],
                                 created_at=str(datetime.date.today()))
        db.update_product_quantity(product_id=product[0], quantity=quantity)

        # for analits
        # incoming payment

        await message.answer("Product quantity successfully updated", reply_markup=users_button)
        await state.clear()
    else:
        await message.answer("In stock does not enough product to sell the product", reply_markup=users_button)

"""Add"""


@dp.message(F.text == "Add Product")
async def add_product(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    await message.answer("Please wait !")
    titles = create_menu(take=user.take, skip=user.skip, database=db)
    menu_button = InlineKeyboardBuilder()
    menu_button.row(InlineKeyboardButton(text="<-previous", callback_data="previous_add_product"),
                    InlineKeyboardButton(text="next->", callback_data="next_add_product"))
    menu = FSInputFile("media/menu_of_products/menu.jpg")
    await bot.send_photo(chat_id=message.from_user.id, photo=menu,
                         reply_markup=menu_button.as_markup())
    titles_button = []
    for i in titles:
        titles_button.append([KeyboardButton(text=i)])
    title_ = ReplyKeyboardMarkup(keyboard=titles_button,
                                 resize_keyboard=True
                                 )
    await bot.send_message(chat_id = message.from_user.id, text="Select product to add", reply_markup=title_)
    await state.set_state(ProductStates.add_product)


@dp.message(ProductStates.add_product)
async def add_product_continue_part_1(message: types.Message, state: FSMContext):
    product = db.get_product_by_product_code(message.text)
    if product is None:
        await message.answer("No product. Please Enter product code without any extra charters.")
    else:
        product_photos = db.get_photo_by_product_id(product[0])
        for i in product_photos:
            await message.answer_photo(FSInputFile(i[2]))
        product_photo = FSInputFile(product_photos[0][2])
        users = get_user(str(message.from_user.id))
        users.added_product = product[1]
        user = db.get_user_by_id(product[3])
        await message.answer_photo(product_photo,
                                   caption=f"Product Code: {product[1]},\nProduct Description: {product[3]},\nCreated By: {user[1]},\nCreate at: {product[5]}\nPrice: {product[6]}, \nQuantity: {product[6]}")
        await message.answer("Please enter quantity : ")
        await state.set_state(ProductStates.added_product)



@dp.message(ProductStates.added_product)
async def add_product_continue_part_2(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    product = db.get_product_by_product_code(user.added_product)
    try:
        creater = db.get_user_by_telegra_id(message.from_user.id)
        adding = int(message.text)

        # for analits
        # outgoing payment
    except:
        await message.answer("Please enter product quantity without any extra charters.")
    quantity = int(adding) + int(product[6])
    db.update_product_quantity(product_id=product[0], quantity=quantity)
    await message.answer("Product Successfully Added!", reply_markup=users_button)
    await state.clear()
    db.note_outgoing_payment(message.from_user.id, product[1], quantity * product[5], creater[0],
                             created_at=datetime.datetime.today())

"""CHANGE"""


@dp.message(F.text == "Change Product")
async def change_product(message: types.Message, state:FSMContext):
    user = get_user(str(message.from_user.id))
    await message.answer("Please wait !")
    last_product = db.get_last_product()
    titles = create_menu(take=user.take, skip=user.skip, database=db)
    titles_button = []
    for i in titles:
        titles_button.append([KeyboardButton(text=i)])
    title_ = ReplyKeyboardMarkup(keyboard=titles_button,
                                 resize_keyboard=True
                                 )
    await bot.send_photo(chat_id = message.from_user.id, photo=FSInputFile("media/menu_of_products/menu.jpg"), caption="Please enter product code to change", reply_markup=title_)
    await state.set_state(ProductStates.get_product_code_to_change)




@dp.message(ProductStates.get_product_code_to_change)
async def change_product_by_code(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    user.take = 9
    user.skip = 0
    attribut_button = InlineKeyboardBuilder()
    attribut_button.add(InlineKeyboardButton(text = "Product code", callback_data="/product_code"))
    attribut_button.add(InlineKeyboardButton(text = "Description", callback_data="/product_code"))
    attribut_button.add(InlineKeyboardButton(text = "Price", callback_data="/price"))
    attribut_button.add(InlineKeyboardButton(text = "Quantity", callback_data="/quantity"))
    attribut_button.adjust(3)
    product = db.get_product_by_product_code(message.text)
    if product is None:
        await message.answer("Product not found "
                             "\nPlease resend the product code : ")
    else:
        product_ = Product(*product)
        user.change_product = message.text
        photo = db.get_photo_by_product_id(product[0])
        for i in photo:
            await message.answer_photo(FSInputFile(i[2]))
        await message.answer_photo(FSInputFile(i[2]),
                                   caption=f"Product Code : {product_.product_code}\n Price : {product_.price}\n Quantity : {product_.quantity},\nTotal Price: {product_.price * product_.quantity}", reply_markup=users_button)
        await message.answer("Which attributes  do you want to change?\n", reply_markup=attribut_button.as_markup())


@dp.callback_query(F.data.startswith(("/product_code" , "/description", "/price", "/quantity")))
async def change_product_attributes(call: types.CallbackQuery, state: FSMContext):
    user = get_user(str(call.from_user.id))
    attribute = call.data[1:]
    user.attribute = attribute

    if attribute == 'price' or attribute == 'quantity':
        await call.message.answer(f"Enter {attribute}  which you want to change?")
        await state.set_state(ProductStates.change_int_attributes)
    else:
        await call.message.answer(f"Enter {attribute}  which you want to change?")
        await state.set_state(ProductStates.change_str_attributes)



@dp.message(ProductStates.change_int_attributes)
async def change_int_attributes(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    try:
        if user.attribute == "price":
            change = float(message.text)
        else:
            change = int(message.text)
        db.update_product_attributes(product_code=user.change_product, column=user.attribute, new_attributes=change)
        await message.answer(text = (f"{user.attribute}   changed  to {change} successfully"), reply_markup=users_button)
        await state.clear()
    except:
        await message.answer(f"Enter  int number , because {user.attribute} gets  numberic ")

@dp.message(ProductStates.change_str_attributes)
async def change_str_attributes(message: types.Message, state: FSMContext):
    user = get_user(str(message.from_user.id))
    change = message.text
    db.update_product_attributes(product_code=user.change_product, column=user.attribute, new_attributes=change)
    await message.answer(f"{user.attribute} changed to {change} successfully", reply_markup=users_button)
    await state.clear()




