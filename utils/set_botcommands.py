from aiogram import types

commands = [
    types.BotCommand(command='start', description="Botni ishga tushirish"),
    types.BotCommand(command='help', description="Yordam"),
    types.BotCommand(command='all_line_graft',description="Barchar Incoming va Outgoing pullarni line graf visualizatsiyasi"),
    types.BotCommand(command='hist_incoming', description="Incoming pullarni histogram visualizatsiyasi"),
    types.BotCommand(command='bar_incoming', description="Incoming pullarni bar visualizatsiyasi"),
    types.BotCommand(command='pie_incoming', description="Incoming pullarni pie chart visualizatsiyasi"),
    types.BotCommand(command='bar_outgoing', description="outgoing pullarni bar visualizatsiyasi"),
    types.BotCommand(command='hist_outgoing', description="Outgoing pullarni histogram visualizatsiyasi"),
    types.BotCommand(command='pie_outgoing', description="Outgoing pullarni pie chart qilib chiqaradi"),
]
