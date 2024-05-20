
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from utils.analysis.analysts import hist_plot, bar_plot, pie_chart, pie_chart_outgoing, bar_plot_outgoing, \
    hist_plot_outgoing, all_line_graft
from loader import dp, db, bot
from handlers.users.product_part import generate_short_uuid


@dp.message(Command("hist_incoming"))
async def send_histogram(message: types.Message, state: FSMContext):
    await message.answer("Please wait histogram creating.")
    hist = "hist_incoming"
    hist_plot(hist)
    await message.answer_photo(photo=(FSInputFile(f"media/analisis/{hist}.jpg")))


@dp.message(Command("bar_incoming"))
async def send_barplot(message: types.Message, state: FSMContext):
    await message.answer("Please wait bar plot creating.")
    bar = "bar_incoming"
    bar_plot(bar)
    await message.answer_photo(FSInputFile(f"media/analisis/{bar}.jpg"))


@dp.message(Command("pie_incoming"))
async def send_pieplot(message: types.Message, state: FSMContext):
    await message.answer("Please wait pie gram creating.")
    pie = "pie_incoming"
    pie_chart(pie)
    await message.answer_photo(FSInputFile(f"media/analisis/{pie}.jpg"))


@dp.message(Command("hist_outgoing"))
async def send_histogram(message: types.Message, state: FSMContext):
    await message.answer("Please wait histogram creating.")
    hist = "hist_outgoing"
    hist_plot_outgoing(hist)
    await message.answer_photo(photo=(FSInputFile(f"media/analisis/{hist}.jpg")))


@dp.message(Command("bar_outgoing"))
async def send_barplot(message: types.Message, state: FSMContext):
    await message.answer("Please wait bar plot creating.")
    bar = "bar_outgoing"
    bar_plot_outgoing(bar)
    await message.answer_photo(FSInputFile(f"media/analisis/{bar}.jpg"))


@dp.message(Command("pie_outgoing"))
async def send_pieplot(message: types.Message, state: FSMContext):
    await message.answer("Please wait pie gram creating.")
    pie = "pie_outgoing"
    pie_chart_outgoing(pie)
    await message.answer_photo(FSInputFile(f"media/analisis/{pie}.jpg"))


@dp.message(Command("all_line_graft"))
async def send_pieplot(message: types.Message, state: FSMContext):
    await message.answer("Please wait pie gram creating.")
    line = "all_line_graft"
    all_line_graft(line)
    await message.answer_photo(FSInputFile(f"media/analisis/all_line_graft.jpg"))
