import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton

import configure
import parse_site 


API_TOKEN = configure.config["token"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Starting parse with this URL
URL = "https://cats.parts/moto/"
URL_to_R1200RT_K26 = "K26/51559/0:0:200502/"

storage = MemoryStorage()

# Initialize Bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class FSMParts(StatesGroup):
    parts_group = State()
    parts_subgroup = State()
    parts = State()
    shops = State()


# Register handler to select a group
@dp.message_handler(commands=["start", "help"], state=None)
async def fsm_group(message: types.Message, state: FSMContext):
    
    global URL_group
    URL_group = URL + URL_to_R1200RT_K26
    html_text = requests.get(URL_group).text
    group_data = parse_site.get_group(html_text)
    group_kb = ReplyKeyboardMarkup(one_time_keyboard=True,\
        resize_keyboard=True)
    
    await FSMParts.parts_group.set()

    for key in group_data:
        group_kb.add(KeyboardButton(f"{key}\nкод группы: {group_data[key]}"))
    await message.answer("Выберите группу узлов",\
        reply_markup = group_kb) 
    
# Register handler to select a subgroup
@dp.message_handler(state=FSMParts.parts_group)
async def fsm_subgroup(message: types.Message, state: FSMContext):    

    global URL_subgroup
    URL_subgroup = URL_group + message.text.strip()[-2:] + "/"    
    html_text = requests.get(URL_subgroup).text
    subgroup_data = parse_site.get_subgroup(html_text)
    subgroup_kb = ReplyKeyboardMarkup(one_time_keyboard=True,\
        resize_keyboard=True)
    
    await FSMParts.parts_subgroup.set()
     
    for key in subgroup_data:
        subgroup_kb.add(KeyboardButton(f"{key}\nкод узла: {subgroup_data[key]}"))
    await message.answer("Выберите узел",\
        reply_markup = subgroup_kb)
    await message.delete()
    await FSMParts.next()
    
# Register handler to scheme output and select a parts    
@dp.message_handler(state=FSMParts.parts)
async def fsm_parts(message: types.Message, state: FSMContext):
        
    global URL_parts
    URL_parts = URL_subgroup + message.text[-7:] +"/"
    html_text = requests.get(URL_parts).text
    scheme_picture = parse_site.get_scheme(html_text)
    await message.answer(scheme_picture)
    
    parts_data = parse_site.get_parts(html_text)
    parts_kb = ReplyKeyboardMarkup(one_time_keyboard=True,\
        resize_keyboard=True)
    
    await FSMParts.parts.set()
    
    for key in parts_data:
        parts_kb.add(KeyboardButton(f"{key}\nкат. номер: {parts_data[key]}"))
    await message.answer("Выберите деталь и магазин",\
        reply_markup=parts_kb)
    await message.delete()
    await FSMParts.next()
    
# Register handler to select a shop of parts
@dp.message_handler(state=FSMParts.shops)
async def fsm_shops(message: types.Message, state: FSMContext):
    catnumber = message.text[-15:]
    shop_buttons = InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)

    exist_button = InlineKeyboardButton(text="Exist",\
        url=parse_site.get_exist_link(catnumber))
    cats_button = InlineKeyboardButton(text="Cats.parts",\
        url=parse_site.get_cats_link(catnumber))
    zzap_button = InlineKeyboardButton(text="ZZap",\
        url=parse_site.get_zzap_link(catnumber))
    
    shop_buttons.add(exist_button, cats_button, zzap_button)
    await message.answer("Магазины:", reply_markup=shop_buttons)
    await message.delete()
    await message.answer("Для перехода в начало нажмите ➡️ /start ⬅️")
    await state.finish()

   
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)