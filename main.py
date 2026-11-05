import asyncio
import logging
import os
import random
import threading
import uuid
from flask import Flask

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import (
CallbackQuery,
InlineKeyboardButton,
InlineKeyboardMarkup,
InputMediaPhoto,
Message,
)

TOKEN = os.getenv("BOTTOKEN", "8947362428:AAFMBUvYa_l3ThqiJrt24zKDOxxKjhZS9H8")
BOT_NAME = "bakugangame_bot"

web_app = Flask(__name__)

@web_app.route('/')
def home():
return 'Bakugan Arena Server is Live!'

def run_web_server():
port = int(os.getenv("PORT", 8080))
web_app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

ELEMS = {
'Pyrus': '🔥 Пайрус',
'Aquos': '💧 Аквос',
'Haos': '⚡ Хаос',
'Ventus': '🍃 Вентус',
'Subterra': '🪨 Саптера',
'Darkus': '🌑 Даркус'
}

ADV = {
'Pyrus': 'Ventus',
'Ventus': 'Subterra',
'Subterra': 'Darkus',
'Darkus': 'Aquos',
'Aquos': 'Pyrus',
'Haos': 'Darkus'
}

RAW_BAKUGANS = [
# Сезон 1: Battle Brawlers
("Dragonoid", "Pyrus", 340, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Delta Dragonoid", "Pyrus", 450, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Ultimate Dragonoid", "Pyrus", 550, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Pyrus Griffon", "Pyrus", 330, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Pyrus Falconeer", "Pyrus", 320, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Pyrus Saurus", "Pyrus", 370, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Preyas", "Aquos", 340, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Sirenoid", "Aquos", 370, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Aquos Siege", "Aquos", 380, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Aquos Limulus", "Aquos", 320, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Aquos Juggernoid", "Aquos", 300, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Tigrerra", "Haos", 340, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Blade Tigrerra", "Haos", 450, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Tentaclear", "Haos", 370, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Haos Hynoid", "Haos", 310, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Haos Freezer", "Haos", 330, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Skyress", "Ventus", 360, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Storm Skyress", "Ventus", 450, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Harpus", "Ventus", 370, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Monarus", "Ventus", 330, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Ventus Ravenoid", "Ventus", 350, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Gorem", "Subterra", 380, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Hammer Gorem", "Subterra", 450, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Subterra Cycloid", "Subterra", 370, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Subterra Tuskor", "Subterra", 350, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Subterra Wormquake", "Subterra", 320, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Hydranoid", "Darkus", 400, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Dual Hydranoid", "Darkus", 480, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Alpha Hydranoid", "Darkus", 550, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Darkus Reaper", "Darkus", 370, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Darkus Fear Ripper", "Darkus", 360, "Сезон 1: Battle Brawlers", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),

# Сезон 2: New Vestroia
("Neo Dragonoid", "Pyrus", 400, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Cross Dragonoid", "Pyrus", 600, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Helix Dragonoid", "Pyrus", 650, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Helios", "Pyrus", 460, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Viper Helios", "Pyrus", 520, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Cyborg Helios", "Pyrus", 620, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Preyas II", "Aquos", 430, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Elfin", "Aquos", 400, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Minx Elfin", "Aquos", 520, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Elico", "Aquos", 500, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Blast Elico", "Aquos", 600, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Nemus", "Haos", 450, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Saint Nemus", "Haos", 550, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Mega Brontes", "Haos", 480, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Alto Brontes", "Haos", 560, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Ingram", "Ventus", 460, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Master Ingram", "Ventus", 540, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Ventus Altair", "Ventus", 500, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Wired", "Ventus", 410, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Hawktor", "Ventus", 490, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Wilda", "Subterra", 450, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Magma Wilda", "Subterra", 560, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Primo Vulcan", "Subterra", 480, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Rex Vulcan", "Subterra", 580, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Coredem", "Subterra", 510, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Percival", "Darkus", 470, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Midnight Percival", "Darkus", 550, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Linehalt", "Darkus", 500, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Helios MK2", "Darkus", 670, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Hades", "Darkus", 600, "Сезон 2: New Vestroia", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),

# Сезон 3: Gundalian Invaders
("Maxus Dragonoid", "Pyrus", 680, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Hyper Dragonoid", "Pyrus", 480, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Pyrus Verias", "Pyrus", 410, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Abis Omega", "Aquos", 420, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Macubass", "Aquos", 620, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Aranaut", "Haos", 500, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Boriates", "Haos", 610, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Dynamo", "Haos", 420, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Strikeflier", "Ventus", 520, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Aluze", "Ventus", 610, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Dryoid", "Subterra", 630, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Scraper", "Subterra", 420, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Exedra", "Darkus", 500, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Naga", "Darkus", 520, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E"),
("Farbros", "Darkus", 690, "Сезон 3: Gundalian Invaders", "https://www.google.com/url?q=https://images.unsplash.com/photo-1578632767115-351597cf2477?w%3D600&source=gmail&ust=1793938882167000&sa=E")
]

BAKUGANS = [
{
'name': item[0],
'element': item[1],
'g': item[2],
'season': item[3],
'img': item[4]
}
for item in RAW_BAKUGANS
]

GATES = [
{'name': 'Огненный Буст', 'elem': 'Pyrus', 'g': 250, 'desc': 'Дает +250 G бакугану Пайруса'},
{'name': 'Вулкан Пайруса', 'elem': 'Pyrus', 'g': 200, 'desc': 'Дает +200 G бакугану Пайруса'},
{'name': 'Водный Водоворот', 'elem': 'Aquos', 'g': 220, 'desc': 'Дает +220 G бакугану Аквоса'},
{'name': 'Бездна Аквоса', 'elem': 'Aquos', 'g': 180, 'desc': 'Дает +180 G бакугану Аквоса'},
{'name': 'Священный Свет', 'elem': 'Haos', 'g': 280, 'desc': 'Дает +280 G бакугану Хаоса'},
{'name': 'Сияние Хаоса', 'elem': 'Haos', 'g': 200, 'desc': 'Дает +200 G бакугану Хаоса'},
{'name': 'Тайфун Ветра', 'elem': 'Ventus', 'g': 230, 'desc': 'Дает +230 G бакугану Вентусу'},
{'name': 'Шторм Вентуса', 'elem': 'Ventus', 'g': 190, 'desc': 'Дает +190 G бакугану Вентусу'},
{'name': 'Гравитация Земли', 'elem': 'Subterra', 'g': 240, 'desc': 'Дает +240 G бакугану Саптеры'},
{'name': 'Каньон Саптеры', 'elem': 'Subterra', 'g': 200, 'desc': 'Дает +200 G бакугану Саптеры'},
{'name': 'Зазеркалье Тьмы', 'elem': 'Darkus', 'g': 260, 'desc': 'Дает +260 G бакугану Даркуса'},
{'name': 'Пропасть Даркуса', 'elem': 'Darkus', 'g': 210, 'desc': 'Дает +210 G бакугану Даркуса'},
{'name': 'Поле Боя', 'elem': 'Any', 'g': 150, 'desc': 'Дает +150 G любому бакугану'},
{'name': 'Арена Силы', 'elem': 'Any', 'g': 100, 'desc': 'Дает +100 G любому бакугану'}
]

ABILS = [
{'name': 'Огненный залп', 'elem': 'Pyrus', 'g': 180, 'h': 0, 'desc': 'Атака пламенем: +180 G'},
{'name': 'Удар Дракона', 'elem': 'Pyrus', 'g': 250, 'h': 0, 'desc': 'Мощный рывок: +250 G'},
{'name': 'Водный Барьер', 'elem': 'Aquos', 'g': 160, 'h': 0, 'desc': 'Волна защиты: +160 G'},
{'name': 'Лечение Океана', 'elem': 'Aquos', 'g': 0, 'h': 150, 'desc': 'Восстанавливает +150 HP игроку'},
{'name': 'Ослепляющий Свет', 'elem': 'Haos', 'g': 190, 'h': 0, 'desc': 'Вспышка света: +190 G'},
{'name': 'Очищение', 'elem': 'Haos', 'g': 0, 'h': 200, 'desc': 'Исцеление светом: +200 HP игроку'},
{'name': 'Штормовой Всплеск', 'elem': 'Ventus', 'g': 210, 'h': 0, 'desc': 'Ураганный порыв: +210 G'},
{'name': 'Воздушный Клинок', 'elem': 'Ventus', 'g': 170, 'h': 0, 'desc': 'Режущий ветер: +170 G'},
{'name': 'Каменный Панцирь', 'elem': 'Subterra', 'g': 220, 'h': 0, 'desc': 'Укрепление брони: +220 G'},
{'name': 'Землетрясение', 'elem': 'Subterra', 'g': 190, 'h': 0, 'desc': 'Раскол арены: +190 G'},
{'name': 'Теневой Коготь', 'elem': 'Darkus', 'g': 230, 'h': 0, 'desc': 'Удар из тьмы: +230 G'},
{'name': 'Поглощение Тьмы', 'elem': 'Darkus', 'g': 120, 'h': 100, 'desc': 'Вампиризм: +120 G и +100 HP'},
{'name': 'Универсал', 'elem': 'Any', 'g': 120, 'h': 0, 'desc': 'Базовое усиление: +120 G'},
{'name': 'Аптечка', 'elem': 'Any', 'g': 0, 'h': 100, 'desc': 'Первая помощь: +100 HP игроку'}
]

QUIT_BUTTON = InlineKeyboardButton(text="🏳️ Выйти в меню", callback_data="quit")

def format_bakugan_string(b):
return f"{b['name']} ({ELEMS[b['element']]}) [{b['season']}]"

class Player:
def __init__(self, user_id, name, is_bot=False):
self.uid = user_id
https://www.google.com/url?q=http://self.name&source=gmail&ust=1793938882167000&sa=E = name
self.is_bot = is_bot
self.hp = 1000
self.team = []
self.gates = []
self.abils = []
self.d_elem = 'Pyrus'
self.d_idx = 0
self.stage = 'baku'
self.baku = None
self.gate = None
self.used_abils = []
self.gate_on = False
self.done = False
self.act_text = ""
self.mid = None

def get_elements(self):
return {b['element'] for b in self.team} | {'Any'}

def get_valid_gates(self):
return [g for g in GATES if g['elem'] in self.get_elements()]

def get_valid_abils(self):
return [a for a in ABILS if a['elem'] in self.get_elements()]

def check_stage(self):
if len(self.team) < 3:
self.stage = 'baku'
elif not self.gates:
self.stage = 'gate'
elif not self.abils:
self.stage = 'abil'
else:
self.stage = 'ready'

def reset_round(self):
self.baku = None
self.gate = None
self.used_abils = []
self.gate_on = False
self.done = False
self.act_text = ""

class Game:
def __init__(self, room_id, p1, is_bot=False):
self.rid = room_id
self.p1 = p1
self.phase = 'draft'
self.step = 1
self.p2 = Player(0, "🤖 ИИ", True) if is_bot else None
if is_bot:
self.p2.team = random.sample(BAKUGANS, 3)
self.refill_bot()

def refill_bot(self):
if not self.p2.gates:
val_gates = self.p2.get_valid_gates()
self.p2.gates = random.sample(val_gates, min(3, len(val_gates)))
if not self.p2.abils:
val_abils = self.p2.get_valid_abils()
self.p2.abils = random.sample(val_abils, min(3, len(val_abils)))
self.p2.stage = 'ready'

games = {}
user_game = {}

def get_current_g(p: Player, opp: Player):
if not p.baku:
return 0
g = p.baku['g'] + sum(a['g'] for a in p.used_abils)
if p.gate_on and p.gate and p.gate['elem'] in (p.baku['element'], 'Any'):
g += p.gate['g']
if opp and opp.baku:
if ADV.get(p.baku['element']) == opp.baku['element']:
g += 150
elif ADV.get(opp.baku['element']) == p.baku['element']:
g -= 150
return max(0, g)

async def send_media_or_text(p: Player, photo_url: str, text: str, keyboard: InlineKeyboardMarkup):
if p.is_bot:
return
try:
if photo_url:
if p.mid:
try:
await bot.edit_message_media(
chat_id=p.uid,
message_id=p.mid,
media=InputMediaPhoto(media=photo_url, caption=text, parse_mode="Markdown"),
reply_markup=keyboard
)
return
except Exception:
await bot.delete_message(chat_id=p.uid, message_id=p.mid)
msg = await bot.send_photo(
chat_id=p.uid,
photo=photo_url,
caption=text,
reply_markup=keyboard,
parse_mode="Markdown"
)
p.mid = msg.message_id
else:
if p.mid:
await bot.edit_message_text(
chat_id=p.uid,
message_id=p.mid,
text=text,
reply_markup=keyboard,
parse_mode="Markdown"
)
else:
msg = await bot.send_message(
chat_id=p.uid,
text=text,
reply_markup=keyboard,
parse_mode="Markdown"
)
p.mid = msg.message_id
except Exception as e:
logging.error(f"Error in send_media_or_text: {e}")

def generate_draft_view(p: Player):
if p.stage == 'baku':
cur = [b for b in BAKUGANS if b['element'] == p.d_elem]
b = cur[p.d_idx % len(cur)]
team_txt = "
".join(f"• {format_bakugan_string(x)} — `{x['g']} G`" for x in p.team)
if team_txt:
team_txt = f"Твоя команда:
{team_txt}

"
text = (
f"🛡️ *НАБОР БАКУГАНОВ ({len(p.team)}/3)*
"
f"{team_txt}"
f"Боец: *{format_bakugan_string(b)}*
"
f"Сила: `{b['g']} G`
"
f"Сезон: _{b['season']}_"
)
keyboard = [
[InlineKeyboardButton(text=v[:1], callback_data=f"de_{k}") for k, v in ELEMS.items()],
[
InlineKeyboardButton(text="◀️", callback_data="dp"),
InlineKeyboardButton(text="➕ Взять", callback_data="da"),
InlineKeyboardButton(text="▶️", callback_data="dn")
],
[InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")],
[QUIT_BUTTON]
]
return b['img'], text, InlineKeyboardMarkup(inline_keyboard=keyboard)

elif p.stage == 'gate':
val_gates = p.get_valid_gates()
c = val_gates[p.d_idx % len(val_gates)]
text = (
f"🎴 *ДОБОР КАРТ ВОРОТ ({len(p.gates)}/3)*
"
f"_(Доступны карты под стихии твоих бой)_

"
f"Карта: *{c['name']}* [{ELEMS.get(c['elem'], 'Универсальная')}]
"
f"Эффект: _{c['desc']}_"
)
keyboard = [
[
InlineKeyboardButton(text="◀️", callback_data="dp"),
InlineKeyboardButton(text="➕ Взять", callback_data="da"),
InlineKeyboardButton(text="▶️", callback_data="dn")
],
[InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")],
[QUIT_BUTTON]
]
return None, text, InlineKeyboardMarkup(inline_keyboard=keyboard)

else:
val_abils = p.get_valid_abils()
a = val_abils[p.d_idx % len(val_abils)]
text = (
f"✨ *ДОБОР СПОСОБНОСТЕЙ ({len(p.abils)}/3)*
"
f"_(Доступны способности под стихии твоих бой)_

"
f"Карта: *{a['name']}* [{ELEMS.get(a['elem'], 'Универсальная')}]
"
f"Описание: _{a['desc']}_"
)
keyboard = [
[
InlineKeyboardButton(text="◀️", callback_data="dp"),
InlineKeyboardButton(text="➕ Взять", callback_data="da"),
InlineKeyboardButton(text="▶️", callback_data="dn")
],
[InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")],
[QUIT_BUTTON]
]
return None, text, InlineKeyboardMarkup(inline_keyboard=keyboard)

async def start_or_draft(gm: Game, prefix=""):
p1, p2 = gm.p1, gm.p2
if p2.is_bot:
gm.refill_bot()
p1.check_stage()
p2.check_stage()

if p1.stage == 'ready' and p2.stage == 'ready':
gm.phase = 'gate'
for p in (p1, p2):
if p.is_bot:
continue
keyboard_rows = [
[InlineKeyboardButton(text=f"{g['name']} ({g['desc']})", callback_data=f"sg_{i}")]
for i, g in enumerate(p.gates)
]
keyboard_rows.append([QUIT_BUTTON])
await send_media_or_text(
p,
p.team[0]['img'],
f"{prefix}🎴 *Установи Карту Ворот взакрытую:*",
InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
)
else:
gm.phase = 'draft'
for p in (p1, p2):
if p.is_bot:
continue
if p.stage != 'ready':
img, text, kb = generate_draft_view(p)
await send_media_or_text(p, img, f"{prefix}🔄 *Нужен добор карт:*

{text}", kb)
else:
await send_media_or_text(
p,
None,
f"{prefix}⏳ Ждем, пока соперник наберет карты...",
InlineKeyboardMarkup(inline_keyboard=[[QUIT_BUTTON]])
)

async def run_round_lifecycle(gm: Game):
p1, p2 = gm.p1, gm.p2

if gm.phase == 'gate':
if p1.done and (p2.done or p2.is_bot):
if p2.is_bot:
p2.gate = p2.gates.pop(0)
gm.phase = 'baku'
p1.done, p2.done = False, False
for p in (p1, p2):
if p.is_bot:
continue
keyboard_rows = [
[InlineKeyboardButton(text=f"{format_bakugan_string(b)} — {b['g']} G", callback_data=f"sb_{i}")]
for i, b in enumerate(p.team)
]
keyboard_rows.append([QUIT_BUTTON])
await send_media_or_text(
p,
p.team[0]['img'],
"👾 *Выбери и брось бакугана взакрытую:*",
InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
)

elif gm.phase == 'baku':
if p1.done and (p2.done or p2.is_bot):
if p2.is_bot:
p2.baku = random.choice(p2.team)
gm.phase = 'tactics'
gm.step = 1
p1.done, p2.done = False, False
await next_tactical_step(gm)

elif gm.phase == 'tactics':
if p2.is_bot and not p2.done:
if p2.abils and random.choice([True, False]):
ability = p2.abils.pop(0)
p2.used_abils.append(ability)
p2.hp = min(1000, p2.hp + ability['h'])
p2.act_text = f"сыграл «{ability['name']}» ({ability['desc']})"
elif p2.gate and not p2.gate_on:
p2.gate_on = True
p2.act_text = f"открыл «{p2.gate['name']}» ({p2.gate['desc']})"
else:
p2.act_text = "пропустил шаг"
p2.done = True

if p1.done and p2.done:
step_summary = f"⚡ *Итог шага {gm.step}:*
• {https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793938882167000&sa=E}: {p1.act_text}
• {https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793938882167000&sa=E}: {p2.act_text}

"
if gm.step < 3:
gm.step += 1
p1.done, p2.done = False, False
await next_tactical_step(gm, step_summary)
else:
g1 = get_current_g(p1, p2)
g2 = get_current_g(p2, p1)
dmg = min(500, max(250, abs(g1 - g2)))
if g1 > g2:
p2.hp = max(0, p2.hp - dmg)
round_res = f"🏆 Раунд за {https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793938882167000&sa=E}! Урон: `{dmg}`"
elif g2 > g1:
p1.hp = max(0, p1.hp - dmg)
round_res = f"🏆 Раунд за {https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793938882167000&sa=E}! Урон: `{dmg}`"
else:
round_res = "🤝 Ничья!"

full_res = (
f"{step_summary}🏁 *Финал раунда ({g1}G vs {g2}G):* {round_res}
"
f"❤️ HP: {https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793938882167000&sa=E} `{p1.hp}` | {https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793938882167000&sa=E} `{p2.hp}`

"
)

if p1.hp <= 0 or p2.hp <= 0:
winner_name = https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793938882167000&sa=E if p2.hp <= 0 else https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793938882167000&sa=E
for p in (p1, p2):
await send_media_or_text(
p,
p.baku['img'],
f"{full_res}👑 *ПОБЕДИЛ {winner_name}!*",
InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔄 В главное меню", callback_data="menu")]])
)
games.pop(gm.rid, None)
return

p1.reset_round()
p2.reset_round()
await start_or_draft(gm, full_res)

async def next_tactical_step(gm: Game, prefix=""):
for p, opp in ((gm.p1, gm.p2), (gm.p2, gm.p1)):
if p.is_bot:
continue
keyboard_rows = [
[InlineKeyboardButton(text=f"✨ {a['name']} ({a['desc']})", callback_data=f"sa_{i}")]
for i, a in enumerate(p.abils)
]
if p.gate and not p.gate_on:
keyboard_rows.append([InlineKeyboardButton(text=f"💥 Открыть Ворота: {p.gate['name']}", callback_data="s_open")])
keyboard_rows.append([InlineKeyboardButton(text="⏩ Пропустить шаг (Пасс)", callback_data="s_pass")])
keyboard_rows.append([QUIT_BUTTON])

status_text = (
f"{prefix}⚔️ *ТАКТИЧЕСКИЙ БОЙ (Шаг {gm.step}/3)*
"
f"🟢 Ты ({https://www.google.com/url?q=http://p.name&source=gmail&ust=1793938882167000&sa=E}) — HP: `{p.hp}`
"
f"Боец: *{format_bakugan_string(p.baku)}* | Сила: `{get_current_g(p, opp)} G`

"
f"🔴 Враг ({https://www.google.com/url?q=http://opp.name&source=gmail&ust=1793938882167000&sa=E}) — HP: `{opp.hp}`
"
f"Боец: *{format_bakugan_string(opp.baku)}* | Сила: `{get_current_g(opp, p)} G`"
)
await send_media_or_text(p, p.baku['img'], status_text, InlineKeyboardMarkup(inline_keyboard=keyboard_rows))

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject = None):
args = command.args if command else None
if args and args in games and not games[args].p2:
gm = games[args]
gm.p2 = Player(https://www.google.com/url?q=http://message.from_user.id&source=gmail&ust=1793938882167000&sa=E, message.from_user.full_name)
user_game[https://www.google.com/url?q=http://message.from_user.id&source=gmail&ust=1793938882167000&sa=E] = args
img1, t1, k1 = generate_draft_view(gm.p1)
await send_media_or_text(gm.p1, img1, t1, k1)
img2, t2, k2 = generate_draft_view(gm.p2)
await send_media_or_text(gm.p2, img2, t2, k2)
return

keyboard = [
[InlineKeyboardButton(text="⚔️ Играть с Ботом", callback_data="m_bot")],
[InlineKeyboardButton(text="👥 Играть с кентом (PvP)", callback_data="m_pvp")]
]
await message.answer("🔥 *АРЕНА БАКУГАН: ГЛАВНОЕ МЕНЮ*", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="Markdown")

@router.callback_query(F.data == "quit")
async def cb_quit(call: CallbackQuery):
await call.answer("Вы вышли из матча")
rid = user_game.pop(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E, None)
if rid and rid in games:
gm = games.pop(rid)
opp = gm.p2 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p1
if opp and not opp.is_bot:
user_game.pop(opp.uid, None)
menu_btn = [[InlineKeyboardButton(text="🔄 В меню", callback_data="menu")]]
await send_media_or_text(opp, opp.team[0]['img'] if opp.team else None, "🏳️ *Соперник покинул игру! Победа за тобой!*", InlineKeyboardMarkup(inline_keyboard=menu_btn))

keyboard = [
[InlineKeyboardButton(text="⚔️ Играть с Ботом", callback_data="m_bot")],
[InlineKeyboardButton(text="👥 Играть с кентом (PvP)", callback_data="m_pvp")]
]
await call.message.edit_text("🔥 *АРЕНА БАКУГАН: ГЛАВНОЕ МЕНЮ*", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="Markdown")

@router.callback_query(F.data.in_(["m_bot", "m_pvp", "menu"]))
async def cb_menu(call: CallbackQuery):
await call.answer()
if call.data == "m_bot":
rid = str(uuid.uuid4())[:8]
gm = Game(rid, Player(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E, call.from_user.full_name), True)
games[rid] = gm
user_game[https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E] = rid
gm.p1.mid = call.message.message_id
img, text, kb = generate_draft_view(gm.p1)
await send_media_or_text(gm.p1, img, text, kb)
elif call.data == "m_pvp":
rid = str(uuid.uuid4())[:6]
gm = Game(rid, Player(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E, call.from_user.full_name))
games[rid] = gm
user_game[https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E] = rid
gm.p1.mid = call.message.message_id
text = (
f"👥 *Комната создана!*
"
f"Перешли код/ссылку кенту для входа через команду:
"
f"/start {rid}

"
f"⏳ Ждем подключения..."
)
await call.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[QUIT_BUTTON]]), parse_mode="Markdown")
else:
keyboard = [
[InlineKeyboardButton(text="⚔️ Играть с Ботом", callback_data="m_bot")],
[InlineKeyboardButton(text="👥 Играть с кентом (PvP)", callback_data="m_pvp")]
]
await call.message.edit_text("🔥 *АРЕНА БАКУГАН: ГЛАВНОЕ МЕНЮ*", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="Markdown")

@router.callback_query(F.data.startswith("de_"))
async def cb_draft_elem(call: CallbackQuery):
gm = games.get(user_game.get(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E))
if not gm:
return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p2
p.d_elem = call.data[3:]
p.d_idx = 0
img, text, kb = generate_draft_view(p)
await send_media_or_text(p, img, text, kb)

@router.callback_query(F.data.in_(["dp", "dn", "da", "dr"]))
async def cb_draft_nav(call: CallbackQuery):
await call.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E))
if not gm:
return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p2

if call.data == "dp":
p.d_idx -= 1
elif call.data == "dn":
p.d_idx += 1
elif call.data == "dr":
if p.stage == 'baku':
p.team = random.sample(BAKUGANS, 3)
elif p.stage == 'gate':
val_gates = p.get_valid_gates()
p.gates = random.sample(val_gates, min(3, len(val_gates)))
elif p.stage == 'abil':
val_abils = p.get_valid_abils()
p.abils = random.sample(val_abils, min(3, len(val_abils)))
p.d_idx = 0
p.check_stage()
elif call.data == "da":
if p.stage == 'baku':
cur = [b for b in BAKUGANS if b['element'] == p.d_elem]
item = cur[p.d_idx % len(cur)]
if item not in p.team:
p.team.append(item)
if len(p.team) >= 3:
p.d_idx = 0
p.check_stage()
elif p.stage == 'gate':
val_gates = p.get_valid_gates()
item = val_gates[p.d_idx % len(val_gates)]
if item not in p.gates:
p.gates.append(item)
if len(p.gates) >= 3:
p.d_idx = 0
p.check_stage()
elif p.stage == 'abil':
val_abils = p.get_valid_abils()
item = val_abils[p.d_idx % len(val_abils)]
if item not in p.abils:
p.abils.append(item)
if len(p.abils) >= 3:
p.d_idx = 0
p.check_stage()

if p.stage == 'ready':
await start_or_draft(gm)
else:
img, text, kb = generate_draft_view(p)
await send_media_or_text(p, img, text, kb)

@router.callback_query(F.data.startswith("sg_"))
async def cb_set_gate(call: CallbackQuery):
await call.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E))
if not gm:
return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p2
p.gate = p.gates.pop(int(call.data[3:]))
p.done = True
await send_media_or_text(p, p.team[0]['img'], "🎴 Ворота установлены! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BUTTON]]))
await run_round_lifecycle(gm)

@router.callback_query(F.data.startswith("sb_"))
async def cb_set_bakugan(call: CallbackQuery):
await call.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E))
if not gm:
return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p2
p.baku = p.team[int(call.data[3:])]
p.done = True
await send_media_or_text(p, p.baku['img'], f"👾 Брошен *{format_bakugan_string(p.baku)}*! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BUTTON]]))
await run_round_lifecycle(gm)

@router.callback_query(F.data.startswith("sa_"))
async def cb_set_ability(call: CallbackQuery):
await call.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E))
if not gm:
return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p2
ability = p.abils.pop(int(call.data[3:]))
p.used_abils.append(ability)
p.hp = min(1000, p.hp + ability['h'])
p.act_text = f"сыграл «{ability['name']}» ({ability['desc']})"
p.done = True
await send_media_or_text(p, p.baku['img'], "✨ Карта сыграна! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BUTTON]]))
await run_round_lifecycle(gm)

@router.callback_query(F.data == "s_open")
async def cb_open_gate(call: CallbackQuery):
await call.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E))
if not gm:
return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p2
p.gate_on = True
p.act_text = f"открыл «{p.gate['name']}» ({p.gate['desc']})"
p.done = True
await send_media_or_text(p, p.baku['img'], "💥 Ворота открыты! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BUTTON]]))
await run_round_lifecycle(gm)

@router.callback_query(F.data == "s_pass")
async def cb_pass_step(call: CallbackQuery):
await call.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E))
if not gm:
return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://call.from_user.id&source=gmail&ust=1793938882168000&sa=E else gm.p2
p.act_text = "пропустил шаг"
p.done = True
await send_media_or_text(p, p.baku['img'], "⏩ Пасс! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BUTTON]]))
await run_round_lifecycle(gm)

async def main():
logging.basicConfig(level=logging.INFO)
await bot.delete_webhook(drop_pending_updates=True)
await dp.start_polling(bot)

if __name__ == '__main__':
asyncio.run(main())
