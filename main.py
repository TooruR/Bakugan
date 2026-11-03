import os
import asyncio
import logging
import random
import threading
import uuid
from flask import Flask
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# Токен из переменной окружения Render (или локальный фоллбэк)
TOKEN = os.getenv("BOTTOKEN", "8947362428:AAFMBUvYa_l3ThqiJrt24zKDOxxKjhZS9H8")
BOT_USERNAME = "bakugangame_bot"

# ---------- Веб-сервер заглушка для Render ----------
web_app = Flask('')

@web_app.route('/')
def home():
    return 'Bakugan Arena Active'

def run_web():
    port = int(os.getenv("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# ---------- Настройки бота ----------
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

ELEMENTS = {
    'Pyrus': '🔥 Пайрус',
    'Aquos': '💧 Аквос',
    'Haos': '⚡ Хаос',
    'Ventus': '🍃 Вентус',
    'Subterra': '🪨 Саптера',
    'Darkus': '🌑 Даркус',
}

ELEMENT_ADVANTAGES = {
    'Pyrus': 'Ventus',
    'Ventus': 'Subterra',
    'Subterra': 'Darkus',
    'Darkus': 'Aquos',
    'Aquos': 'Pyrus',
    'Haos': 'Darkus',
}

# ================= 100 БАКУГАНОВ =================
BAKUGAANS_POOL = [
    # 1 СЕЗОН
    {'name': 'Dragonoid', 'element': 'Pyrus', 'g': 340, 'season': 1},
    {'name': 'Delta Dragonoid', 'element': 'Pyrus', 'g': 450, 'season': 1},
    {'name': 'Ultimate Dragonoid', 'element': 'Pyrus', 'g': 550, 'season': 1},
    {'name': 'Pyrus Griffon', 'element': 'Pyrus', 'g': 330, 'season': 1},
    {'name': 'Pyrus Falconeer', 'element': 'Pyrus', 'g': 320, 'season': 1},
    {'name': 'Pyrus Saurus', 'element': 'Pyrus', 'g': 370, 'season': 1},
    {'name': 'Pyrus Serpenoid', 'element': 'Pyrus', 'g': 310, 'season': 1},
    {'name': 'Pyrus Robotallion', 'element': 'Pyrus', 'g': 350, 'season': 1},
    {'name': 'Pyrus Mantris', 'element': 'Pyrus', 'g': 390, 'season': 1},
    {'name': 'Preyas', 'element': 'Aquos', 'g': 340, 'season': 1},
    {'name': 'Sirenoid', 'element': 'Aquos', 'g': 370, 'season': 1},
    {'name': 'Aquos Siege', 'element': 'Aquos', 'g': 380, 'season': 1},
    {'name': 'Aquos Limulus', 'element': 'Aquos', 'g': 320, 'season': 1},
    {'name': 'Aquos Juggernoid', 'element': 'Aquos', 'g': 300, 'season': 1},
    {'name': 'Aquos Robotallion', 'element': 'Aquos', 'g': 340, 'season': 1},
    {'name': 'Aquos Fear Ripper', 'element': 'Aquos', 'g': 350, 'season': 1},
    {'name': 'Aquos Saurus', 'element': 'Aquos', 'g': 360, 'season': 1},
    {'name': 'Tigrerra', 'element': 'Haos', 'g': 340, 'season': 1},
    {'name': 'Blade Tigrerra', 'element': 'Haos', 'g': 450, 'season': 1},
    {'name': 'Tentaclear', 'element': 'Haos', 'g': 370, 'season': 1},
    {'name': 'Haos Hynoid', 'element': 'Haos', 'g': 310, 'season': 1},
    {'name': 'Haos Freezer', 'element': 'Haos', 'g': 330, 'season': 1},
    {'name': 'Haos Robotallion', 'element': 'Haos', 'g': 350, 'season': 1},
    {'name': 'Haos Falconeer', 'element': 'Haos', 'g': 320, 'season': 1},
    {'name': 'Haos Saurus', 'element': 'Haos', 'g': 360, 'season': 1},
    {'name': 'Skyress', 'element': 'Ventus', 'g': 360, 'season': 1},
    {'name': 'Storm Skyress', 'element': 'Ventus', 'g': 450, 'season': 1},
    {'name': 'Harpus', 'element': 'Ventus', 'g': 370, 'season': 1},
    {'name': 'Monarus', 'element': 'Ventus', 'g': 330, 'season': 1},
    {'name': 'Ventus Ravenoid', 'element': 'Ventus', 'g': 350, 'season': 1},
    {'name': 'Ventus Falconeer', 'element': 'Ventus', 'g': 310, 'season': 1},
    {'name': 'Ventus Griffon', 'element': 'Ventus', 'g': 320, 'season': 1},
    {'name': 'Ventus Robotallion', 'element': 'Ventus', 'g': 340, 'season': 1},
    {'name': 'Gorem', 'element': 'Subterra', 'g': 380, 'season': 1},
    {'name': 'Hammer Gorem', 'element': 'Subterra', 'g': 450, 'season': 1},
    {'name': 'Subterra Cycloid', 'element': 'Subterra', 'g': 370, 'season': 1},
    {'name': 'Subterra Tuskor', 'element': 'Subterra', 'g': 350, 'season': 1},
    {'name': 'Subterra Wormquake', 'element': 'Subterra', 'g': 320, 'season': 1},
    {'name': 'Subterra Centipoid', 'element': 'Subterra', 'g': 330, 'season': 1},
    {'name': 'Subterra Saurus', 'element': 'Subterra', 'g': 360, 'season': 1},
    {'name': 'Clayf', 'element': 'Subterra', 'g': 500, 'season': 1},
    {'name': 'Hydranoid', 'element': 'Darkus', 'g': 400, 'season': 1},
    {'name': 'Dual Hydranoid', 'element': 'Darkus', 'g': 480, 'season': 1},
    {'name': 'Alpha Hydranoid', 'element': 'Darkus', 'g': 550, 'season': 1},
    {'name': 'Darkus Reaper', 'element': 'Darkus', 'g': 370, 'season': 1},
    {'name': 'Darkus Fear Ripper', 'element': 'Darkus', 'g': 360, 'season': 1},
    {'name': 'Darkus Mantris', 'element': 'Darkus', 'g': 340, 'season': 1},
    {'name': 'Darkus Centipoid', 'element': 'Darkus', 'g': 330, 'season': 1},
    {'name': 'Exedra', 'element': 'Darkus', 'g': 500, 'season': 1},
    {'name': 'Naga', 'element': 'Darkus', 'g': 520, 'season': 1},
    # 2 СЕЗОН
    {'name': 'Neo Dragonoid', 'element': 'Pyrus', 'g': 400, 'season': 2},
    {'name': 'Cross Dragonoid', 'element': 'Pyrus', 'g': 600, 'season': 2},
    {'name': 'Helix Dragonoid', 'element': 'Pyrus', 'g': 650, 'season': 2},
    {'name': 'Helios', 'element': 'Pyrus', 'g': 460, 'season': 2},
    {'name': 'Viper Helios', 'element': 'Pyrus', 'g': 520, 'season': 2},
    {'name': 'Cyborg Helios', 'element': 'Pyrus', 'g': 620, 'season': 2},
    {'name': 'Maxus Dragonoid', 'element': 'Pyrus', 'g': 680, 'season': 2},
    {'name': 'Hyper Dragonoid', 'element': 'Pyrus', 'g': 480, 'season': 2},
    {'name': 'Pyrus Verias', 'element': 'Pyrus', 'g': 410, 'season': 2},
    {'name': 'Preyas II', 'element': 'Aquos', 'g': 430, 'season': 2},
    {'name': 'Elfin', 'element': 'Aquos', 'g': 400, 'season': 2},
    {'name': 'Minx Elfin', 'element': 'Aquos', 'g': 520, 'season': 2},
    {'name': 'Elico', 'element': 'Aquos', 'g': 500, 'season': 2},
    {'name': 'Blast Elico', 'element': 'Aquos', 'g': 600, 'season': 2},
    {'name': 'Abis Omega', 'element': 'Aquos', 'g': 420, 'season': 2},
    {'name': 'Akwimos', 'element': 'Aquos', 'g': 490, 'season': 2},
    {'name': 'Macubass', 'element': 'Aquos', 'g': 620, 'season': 2},
    {'name': 'Nemus', 'element': 'Haos', 'g': 450, 'season': 2},
    {'name': 'Saint Nemus', 'element': 'Haos', 'g': 550, 'season': 2},
    {'name': 'Mega Brontes', 'element': 'Haos', 'g': 480, 'season': 2},
    {'name': 'Alto Brontes', 'element': 'Haos', 'g': 560, 'season': 2},
    {'name': 'Aranaut', 'element': 'Haos', 'g': 500, 'season': 2},
    {'name': 'Boriates', 'element': 'Haos', 'g': 610, 'season': 2},
    {'name': 'Dynamo', 'element': 'Haos', 'g': 420, 'season': 2},
    {'name': 'Clawsaurus', 'element': 'Haos', 'g': 430, 'season': 2},
    {'name': 'Ingram', 'element': 'Ventus', 'g': 460, 'season': 2},
    {'name': 'Master Ingram', 'element': 'Ventus', 'g': 540, 'season': 2},
    {'name': 'Ventus Altair', 'element': 'Ventus', 'g': 500, 'season': 2},
    {'name': 'Wired', 'element': 'Ventus', 'g': 410, 'season': 2},
    {'name': 'Hawktor', 'element': 'Ventus', 'g': 490, 'season': 2},
    {'name': 'Atmos', 'element': 'Ventus', 'g': 430, 'season': 2},
    {'name': 'Strikeflier', 'element': 'Ventus', 'g': 520, 'season': 2},
    {'name': 'Aluze', 'element': 'Ventus', 'g': 610, 'season': 2},
    {'name': 'Wilda', 'element': 'Subterra', 'g': 450, 'season': 2},
    {'name': 'Magma Wilda', 'element': 'Subterra', 'g': 560, 'season': 2},
    {'name': 'Primo Vulcan', 'element': 'Subterra', 'g': 480, 'season': 2},
    {'name': 'Rex Vulcan', 'element': 'Subterra', 'g': 580, 'season': 2},
    {'name': 'Coredem', 'element': 'Subterra', 'g': 510, 'season': 2},
    {'name': 'Dryoid', 'element': 'Subterra', 'g': 630, 'season': 2},
    {'name': 'Subterra Verias', 'element': 'Subterra', 'g': 400, 'season': 2},
    {'name': 'Scraper', 'element': 'Subterra', 'g': 420, 'season': 2},
    {'name': 'Percival', 'element': 'Darkus', 'g': 470, 'season': 2},
    {'name': 'Midnight Percival', 'element': 'Darkus', 'g': 550, 'season': 2},
    {'name': 'Hadron', 'element': 'Darkus', 'g': 420, 'season': 2},
    {'name': 'Shadow Percival', 'element': 'Darkus', 'g': 510, 'season': 2},
    {'name': 'Linehalt', 'element': 'Darkus', 'g': 500, 'season': 2},
    {'name': 'Helios MK2', 'element': 'Darkus', 'g': 670, 'season': 2},
    {'name': 'Hades', 'element': 'Darkus', 'g': 600, 'season': 2},
    {'name': 'MAC Spider', 'element': 'Darkus', 'g': 620, 'season': 2},
    {'name': 'Farbros', 'element': 'Darkus', 'g': 690, 'season': 2},
]

# Карты ворот привязаны к стихиям (или нейтральные)
GATE_CARDS_POOL = [
    {'name': 'Зазеркалье Тьмы', 'element': 'Darkus', 'condition': 'Бакуганы меняются силой', 'type': 'swap_g'},
    {'name': 'Арена Малой Силы', 'element': 'Any', 'condition': 'Побеждает меньшая сила', 'type': 'lowest_wins'},
    {'name': 'Огненное Перевооружение', 'element': 'Pyrus', 'condition': 'Пайрус +250 G, остальные -50 G', 'type': 'pyrus_boost'},
    {'name': 'Священный Уравнитель', 'element': 'Haos', 'condition': 'Силы бойцов уравниваются', 'type': 'equalize_g'},
    {'name': 'Взрывной Резонанс', 'element': 'Pyrus', 'condition': 'Удваивает урон по HP проигравшему', 'type': 'double_damage'},
    {'name': 'Зеркальное Отражение', 'element': 'Aquos', 'condition': 'Копирует G-силу соперника', 'type': 'mirror_power'},
    {'name': 'Кибер-Перехват', 'element': 'Ventus', 'condition': 'Аннулирует способность соперника', 'type': 'nullify_opp_ability'},
    {'name': 'Сердце Новой Вестрои', 'element': 'Subterra', 'condition': 'Удваивает базовую силу бакугана', 'type': 'double_base_g'},
    {'name': 'Вексос-Вампиризм', 'element': 'Darkus', 'condition': 'Победитель восстанавливает HP уроном', 'type': 'vampirism'},
    {'name': 'Анти-Стихийная Арена', 'element': 'Any', 'condition': 'Инверсия преимуществ стихий', 'type': 'element_inversion'},
    {'name': 'Критический Импульс', 'element': 'Haos', 'condition': 'Прибавляет +300 G к вашей силе', 'type': 'flat_300'},
    {'name': 'Водный Водоворот', 'element': 'Aquos', 'condition': 'Отнимает -150 G у врага', 'type': 'flat_sub150'},
    {'name': 'Гравитация Земли', 'element': 'Subterra', 'condition': '+200 G бойцу Саптеры', 'type': 'subterra_boost'},
    {'name': 'Тайфун Ветра', 'element': 'Ventus', 'condition': '+200 G бойцу Вентуса', 'type': 'ventus_boost'}
]

# Способности привязаны к стихиям (или нейтральные)
ABILITIES_POOL = [
    {'name': 'Огненный залп (+180 G)', 'element': 'Pyrus', 'bonus': 180, 'heal': 0},
    {'name': 'Удар Дракона (+250 G)', 'element': 'Pyrus', 'bonus': 250, 'heal': 0},
    {'name': 'Водный Барьер (+150 G)', 'element': 'Aquos', 'bonus': 150, 'heal': 0},
    {'name': 'Лечение Океана (+150 HP)', 'element': 'Aquos', 'bonus': 0, 'heal': 150},
    {'name': 'Ослепляющий Свет (+160 G)', 'element': 'Haos', 'bonus': 160, 'heal': 0},
    {'name': 'Очищение (+200 HP)', 'element': 'Haos', 'bonus': 0, 'heal': 200},
    {'name': 'Штормовой Всплеск (+200 G)', 'element': 'Ventus', 'bonus': 200, 'heal': 0},
    {'name': 'Удар Воздушного Клинка (+170 G)', 'element': 'Ventus', 'bonus': 170, 'heal': 0},
    {'name': 'Каменный Панцирь (+220 G)', 'element': 'Subterra', 'bonus': 220, 'heal': 0},
    {'name': 'Землетрясение (+190 G)', 'element': 'Subterra', 'bonus': 190, 'heal': 0},
    {'name': 'Теневой Коготь (+220 G)', 'element': 'Darkus', 'bonus': 220, 'heal': 0},
    {'name': 'Поглощение Тьмы (+100 G, +100 HP)', 'element': 'Darkus', 'bonus': 100, 'heal': 100},
    {'name': 'Универсальное Усиление (+120 G)', 'element': 'Any', 'bonus': 120, 'heal': 0},
    {'name': 'Полевой Щит (+100 G, +50 HP)', 'element': 'Any', 'bonus': 100, 'heal': 50}
]

RULES_TEXT = (
    "📜 **ПРАВИЛА ИГРЫ «БИТВА БАКУГАН»**\n\n"
    "1. **Драфт команды:** Сначала выбирается 3 бакугана, затем под их стихии подбираются 3 Карты Ворот и 3 Карты Способностей (вручную или рандомом).\n"
    "2. **Скрытые ходы:** Игроки делают выбор взакрытую. Оппонент не видит твой ход, пока не сделает свой!\n"
    "3. **Фазы раунда:**\n"
    "   • Установка Карты Ворот взакрытую.\n"
    "   • Бросок Бакугана на поле.\n"
    "   • 3 Тактических шага (разыгрывание карт или открытие ворот).\n"
    "4. **Анализ:** После каждого одновременного вскрытия дается 10-секундная тактическая пауза.\n"
    "5. **Урон:** Разница в G-силе конвертируется в урон по HP (от 250 до 500). Цель: опустить HP врага с 1000 до 0!"
)

# ---------- Состояние игроков и матча ----------
class PlayerState:
    def __init__(self, user_id, name, is_bot=False):
        self.user_id = user_id
        self.name = name
        self.is_bot = is_bot
        self.hp = 1000

        self.team_baku = []
        self.gate_hand = []
        self.ability_hand = []

        # Индексы для драфта
        self.draft_stage = 'baku' # 'baku' -> 'gate' -> 'ability' -> 'ready'
        self.draft_element = 'Pyrus'
        self.draft_idx = 0

        # Выборы раунда
        self.idx_gate = 0
        self.idx_baku = 0
        self.idx_ability = 0

        self.placed_gate = None
        self.chosen_baku = None
        self.chosen_abilities = []
        self.gate_activated = False

        self.action_done = False
        self.last_action_desc = ""
        self.last_message_id = None

    def get_team_elements(self):
        elems = {b['element'] for b in self.team_baku}
        elems.add('Any')
        return elems

    def reset_round_selection(self):
        self.idx_gate = 0
        self.idx_baku = 0
        self.idx_ability = 0
        self.placed_gate = None
        self.chosen_baku = None
        self.chosen_abilities = []
        self.gate_activated = False
        self.action_done = False
        self.last_action_desc = ""

class Match:
    def __init__(self, room_id, p1_id, p1_name, is_bot_match=False):
        self.room_id = room_id
        self.is_bot_match = is_bot_match
        self.phase = 'draft' # draft, gate_phase, baku_phase, tactical_phase, round_end
        self.sub_turn = 1
        self.p1 = PlayerState(p1_id, p1_name)

        if is_bot_match:
            self.p2 = PlayerState(user_id=0, name="🤖 ИИ Бот", is_bot=True)
            self.p2.team_baku = random.sample(BAKUGAANS_POOL, 3)
            bot_elems = self.p2.get_team_elements()
            compat_gates = [c for c in GATE_CARDS_POOL if c['element'] in bot_elems]
            compat_abils = [c for c in ABILITIES_POOL if c['element'] in bot_elems]
            self.p2.gate_hand = random.sample(compat_gates, min(3, len(compat_gates)))
            self.p2.ability_hand = random.sample(compat_abils, min(3, len(compat_abils)))
            self.p2.draft_stage = 'ready'
        else:
            self.p2 = None

    def is_full(self):
        return self.p2 is not None

    def get_player(self, user_id):
        if self.p1 and self.p1.user_id == user_id:
            return self.p1
        if self.p2 and self.p2.user_id == user_id:
            return self.p2
        return None

    def get_opponent(self, user_id):
        if self.p1 and self.p1.user_id == user_id:
            return self.p2
        if self.p2 and self.p2.user_id == user_id:
            return self.p1
        return None

matches = {}
user_active_room = {}

def calculate_current_g(player: PlayerState, opponent: PlayerState):
    if not player.chosen_baku:
        return 0

    base_g = player.chosen_baku['g']

    for card in player.chosen_abilities:
        base_g += card.get('bonus', 0)

    # Карта ворот игрока
    if player.placed_gate and player.gate_activated:
        t = player.placed_gate.get('type')
        if t == 'pyrus_boost':
            base_g += 250 if player.chosen_baku['element'] == 'Pyrus' else -50
        elif t == 'flat_300':
            base_g += 300
        elif t == 'double_base_g':
            base_g += player.chosen_baku['g']
        elif t == 'subterra_boost':
            if player.chosen_baku['element'] == 'Subterra': base_g += 200
        elif t == 'ventus_boost':
            if player.chosen_baku['element'] == 'Ventus': base_g += 200

    # Влияние карты ворот оппонента
    if opponent and opponent.placed_gate and opponent.gate_activated:
        opp_t = opponent.placed_gate.get('type')
        if opp_t == 'nullify_opp_ability':
            bonus_sum = sum(c.get('bonus', 0) for c in player.chosen_abilities)
            base_g -= bonus_sum
        elif opp_t == 'flat_sub150':
            base_g -= 150

    # Преимущество стихий
    if opponent and opponent.chosen_baku:
        elem1 = player.chosen_baku['element']
        elem2 = opponent.chosen_baku['element']
        inversion = (opponent.placed_gate and opponent.gate_activated and opponent.placed_gate.get('type') == 'element_inversion')

        if not inversion:
            if ELEMENT_ADVANTAGES.get(elem1) == elem2:
                base_g += 150
            elif ELEMENT_ADVANTAGES.get(elem2) == elem1:
                base_g -= 150
        else:
            if ELEMENT_ADVANTAGES.get(elem2) == elem1:
                base_g += 150
            elif ELEMENT_ADVANTAGES.get(elem1) == elem2:
                base_g -= 150

    return max(0, base_g)

async def send_or_update(bot: Bot, player: PlayerState, text: str, kb: InlineKeyboardMarkup = None):
    if player.is_bot:
        return
    if player.last_message_id:
        try:
            await bot.edit_message_text(chat_id=player.user_id, message_id=player.last_message_id, text=text, reply_markup=kb, parse_mode="Markdown")
            return
        except Exception:
            pass
    msg = await bot.send_message(player.user_id, text, reply_markup=kb, parse_mode="Markdown")
    player.last_message_id = msg.message_id

# ---------- Генераторы меню и интерфейса ----------
def build_main_menu():
    kb = [
        [InlineKeyboardButton(text="⚔️ Играть против ИИ", callback_data="menu_vs_bot")],
        [InlineKeyboardButton(text="👥 Дуэль с кентом (PvP)", callback_data="menu_create_room")],
        [InlineKeyboardButton(text="📖 База: Списки Бакуганов и Карт", callback_data="menu_catalog")],
        [InlineKeyboardButton(text="📜 Правила игры", callback_data="menu_rules")]
    ]
    return "🔥 **АРЕНА БАКУГАН: ГЛАВНОЕ МЕНЮ** 🔥\nВыбери действие для старта:", InlineKeyboardMarkup(inline_keyboard=kb)

def build_baku_draft_view(player: PlayerState):
    filtered = [b for b in BAKUGAANS_POOL if b['element'] == player.draft_element]
    if player.draft_idx >= len(filtered):
        player.draft_idx = 0
    item = filtered[player.draft_idx]

    text = f"🛡️ **ШАГ 1: НАБОР БАКУГАНОВ ({player.name})**\nВыбрано: `{len(player.team_baku)}/3`\n\n"
    if player.team_baku:
        text += "Твои бойцы:\n"
        for b in player.team_baku:
            text += f"• {b['name']} ({ELEMENTS[b['element']]}) — `{b['g']} G`\n"
        text += "\n"

    text += f"Выбор: **{item['name']}**\nСтихия: {ELEMENTS[item['element']]}\nСила: `{item['g']} G`"

    kb = [
        [
            InlineKeyboardButton(text="🔥", callback_data="elem_Pyrus"),
            InlineKeyboardButton(text="💧", callback_data="elem_Aquos"),
            InlineKeyboardButton(text="⚡", callback_data="elem_Haos"),
            InlineKeyboardButton(text="🍃", callback_data="elem_Ventus"),
            InlineKeyboardButton(text="🪨", callback_data="elem_Subterra"),
            InlineKeyboardButton(text="🌑", callback_data="elem_Darkus"),
        ],
        [
            InlineKeyboardButton(text="◀️", callback_data="draft_b_prev"),
            InlineKeyboardButton(text=f"[ {player.draft_idx + 1}/{len(filtered)} ]", callback_data="noop"),
            InlineKeyboardButton(text="▶️", callback_data="draft_b_next"),
        ],
        [InlineKeyboardButton(text="➕ Взять бакугана", callback_data="draft_b_add")],
        [InlineKeyboardButton(text="🎲 3 Случайных бойца", callback_data="draft_b_random")],
        [InlineKeyboardButton(text="🏳️ Выйти в меню", callback_data="quit_match")]
    ]
    return text, InlineKeyboardMarkup(inкий Импульс', 'element': 'Haos', 'condition': 'Прибавляет +300 G к вашей силе', 'type': 'flat_300'},
    {'name': 'Водный Водоворот', 'element': 'Aquos', 'condition': 'Отнимает -150 G у врага', 'type': 'flat_sub150'},
    {'name': 'Гравитация Земли', 'element': 'Subterra', 'condition': '+200 G бойцу Саптеры', 'type': 'subterra_boost'},
    {'name': 'Тайфун Ветра', 'element': 'Ventus', 'condition': '+200 G бойцу Вентуса', 'type': 'ventus_boost'}
]

# Способности привязаны к стихиям (или нейтральные)
ABILITIES_POOL = [
    {'name': 'Огненный залп (+180 G)', 'element': 'Pyrus', 'bonus': 180, 'heal': 0},
    {'name': 'Удар Дракона (+250 G)', 'element': 'Pyrus', 'bonus': 250, 'heal': 0},
    {'name': 'Водный Барьер (+150 G)', 'element': 'Aquos', 'bonus': 150, 'heal': 0},
    {'name': 'Лечение Океана (+150 HP)', 'element': 'Aquos', 'bonus': 0, 'heal': 150},
    {'name': 'Ослепляющий Свет (+160 G)', 'element': 'Haos', 'bonus': 160, 'heal': 0},
    {'name': 'Очищение (+200 HP)', 'element': 'Haos', 'bonus': 0, 'heal': 200},
    {'name': 'Штормовой Всплеск (+200 G)', 'element': 'Ventus', 'bonus': 200, 'heal': 0},
    {'name': 'Удар Воздушного Клинка (+170 G)', 'element': 'Ventus', 'bonus': 170, 'heal': 0},
    {'name': 'Каменный Панцирь (+220 G)', 'element': 'Subterra', 'bonus': 220, 'heal': 0},
    {'name': 'Землетрясение (+190 G)', 'element': 'Subterra', 'bonus': 190, 'heal': 0},
    {'name': 'Теневой Коготь (+220 G)', 'element': 'Darkus', 'bonus': 220, 'heal': 0},
    {'name': 'Поглощение Тьмы (+100 G, +100 HP)', 'element': 'Darkus', 'bonus': 100, 'heal': 100},
    {'name': 'Универсальное Усиление (+120 G)', 'element': 'Any', 'bonus': 120, 'heal': 0},
    {'name': 'Полевой Щит (+100 G, +50 HP)', 'element': 'Any', 'bonus': 100, 'heal': 50}
]

RULES_TEXT = (
    "📜 **ПРАВИЛА ИГРЫ «БИТВА БАКУГАН»**\n\n"
    "1. **Драфт команды:** Сначала выбирается 3 бакугана, затем под их стихии подбираются 3 Карты Ворот и 3 Карты Способностей (вручную или рандомом).\n"
    "2. **Скрытые ходы:** Игроки делают выбор взакрытую. Оппонент не видит твой ход, пока не сделает свой!\n"
    "3. **Фазы раунда:**\n"
    "   • Установка Карты Ворот взакрытую.\n"
    "   • Бросок Бакугана на поле.\n"
    "   • 3 Тактических шага (разыгрывание карт или открытие ворот).\n"
    "4. **Анализ:** После каждого одновременного вскрытия дается 10-секундная тактическая пауза.\n"
    "5. **Урон:** Разница в G-силе конвертируется в урон по HP (от 250 до 500). Цель: опустить HP врага с 1000 до 0!"
)

# ---------- Состояние игроков и матча ----------
class PlayerState:
    def __init__(self, user_id, name, is_bot=False):
        self.user_id = user_id
        self.name = name
        self.is_bot = is_bot
        self.hp = 1000

        self.team_baku = []
        self.gate_hand = []
        self.ability_hand = []

        # Индексы для драфта
        self.draft_stage = 'baku' # 'baku' -> 'gate' -> 'ability' -> 'ready'
        self.draft_element = 'Pyrus'
        self.draft_idx = 0

        # Выборы раунда
        self.idx_gate = 0
        self.idx_baku = 0
        self.idx_ability = 0

        self.placed_gate = None
        self.chosen_baku = None
        self.chosen_abilities = []
        self.gate_activated = False

        self.action_done = False
        self.last_action_desc = ""
        self.last_message_id = None

    def get_team_elements(self):
        elems = {b['element'] for b in self.team_baku}
        elems.add('Any')
        return elems

    def reset_round_selection(self):
        self.idx_gate = 0
        self.idx_baku = 0
        self.idx_ability = 0
        self.placed_gate = None
        self.chosen_baku = None
        self.chosen_abilities = []
        self.gate_activated = False
        self.action_done = False
        self.last_action_desc = ""

class Match:
    def __init__(self, room_id, p1_id, p1_name, is_bot_match=False):
        self.room_id = room_id
        self.is_bot_match = is_bot_match
        self.phase = 'draft' # draft, gate_phase, baku_phase, tactical_phase, round_end
        self.sub_turn = 1
        self.p1 = PlayerState(p1_id, p1_name)

        if is_bot_match:
            self.p2 = PlayerState(user_id=0, name="🤖 ИИ Бот", is_bot=True)
            self.p2.team_baku = random.sample(BAKUGAANS_POOL, 3)
            bot_elems = self.p2.get_team_elements()
            compat_gates = [c for c in GATE_CARDS_POOL if c['element'] in bot_elems]
            compat_abils = [c for c in ABILITIES_POOL if c['element'] in bot_elems]
            self.p2.gate_hand = random.sample(compat_gates, min(3, len(compat_gates)))
            self.p2.ability_hand = random.sample(compat_abils, min(3, len(compat_abils)))
            self.p2.draft_stage = 'ready'
        else:
            self.p2 = None

    def is_full(self):
        return self.p2 is not None

    def get_player(self, user_id):
        if self.p1 and self.p1.user_id == user_id:
            return self.p1
        if self.p2 and self.p2.user_id == user_id:
            return self.p2
        return None

    def get_opponent(self, user_id):
        if self.p1 and self.p1.user_id == user_id:
            return self.p2
        if self.p2 and self.p2.user_id == user_id:
            return self.p1
        return None

matches = {}
user_active_room = {}

def calculate_current_g(player: PlayerState, opponent: PlayerState):
    if not player.chosen_baku:
        return 0

    base_g = player.chosen_baku['g']

    for card in player.chosen_abilities:
        base_g += card.get('bonus', 0)

    # Карта ворот игрока
    if player.placed_gate and player.gate_activated:
        t = player.placed_gate.get('type')
        if t == 'pyrus_boost':
            base_g += 250 if player.chosen_baku['element'] == 'Pyrus' else -50
        elif t == 'flat_300':
            base_g += 300
        elif t == 'double_base_g':
            base_g += player.chosen_baku['g']
        elif t == 'subterra_boost':
            if player.chosen_baku['element'] == 'Subterra': base_g += 200
        elif t == 'ventus_boost':
            if player.chosen_baku['element'] == 'Ventus': base_g += 200

    # Влияние карты ворот оппонента
    if opponent and opponent.placed_gate and opponent.gate_activated:
        opp_t = opponent.placed_gate.get('type')
        if opp_t == 'nullify_opp_ability':
            bonus_sum = sum(c.get('bonus', 0) for c in player.chosen_abilities)
            base_g -= bonus_sum
        elif opp_t == 'flat_sub150':
            base_g -= 150

    
