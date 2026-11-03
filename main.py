import os
import random
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOTTOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище игровых сессий в памяти {chat_id: game_state}
GAMES = {}

# ---------- Игровая логика ----------
class Bakugan:
    def __init__(self, name, attribute, base_g):
        self.name = name
        self.attribute = attribute
        self.base_g = base_g
        self.current_g_power = base_g

    def reset(self):
        self.current_g_power = self.base_g

class AbilityCard:
    def __init__(self, card_id, name, description, effect):
        self.id = card_id
        self.name = name
        self.description = description
        self.effect = effect

    def activate(self, me, enemy):
        self.effect(me, enemy)
        me.current_g_power = max(0, me.current_g_power)
        enemy.current_g_power = max(0, enemy.current_g_power)

def _boost(me, enemy):
    me.current_g_power += 50

def _weaken(me, enemy):
    enemy.current_g_power -= 50

def _swap(me, enemy):
    me.current_g_power, enemy.current_g_power = enemy.current_g_power, me.current_g_power

def make_bakugans():
    pool = [
        Bakugan("Дрэгонойд", "Pyrus", 320),
        Bakugan("Хидранойд", "Darkus", 330),
        Bakugan("Тигрера", "Haos", 310),
        Bakugan("Скайресс", "Ventus", 300),
        Bakugan("Прэйинг Мантис", "Subterra", 340),
        Bakugan("Гоургаройд", "Aquos", 315),
    ]
    random.shuffle(pool)
    return pool[:3], pool[3:]

def make_cards():
    return [
        AbilityCard("boost", "Усиление", "+50G себе", _boost),
        AbilityCard("weaken", "Ослабление", "-50G врагу", _weaken),
        AbilityCard("swap", "Обмен силой", "Смена G местами", _swap),
    ]

def make_gates():
    gates = [
        {"name": "Огненные ворота", "bonuses": {"Pyrus": 80, "Aquos": -30}},
        {"name": "Водные ворота", "bonuses": {"Aquos": 80, "Pyrus": -30}},
        {"name": "Ворота тьмы", "bonuses": {"Darkus": 80, "Haos": -30}},
        {"name": "Ворота света", "bonuses": {"Haos": 80, "Darkus": -30}},
        {"name": "Ворота ветра", "bonuses": {"Ventus": 80, "Subterra": -30}},
        {"name": "Ворота земли", "bonuses": {"Subterra": 80, "Ventus": -30}},
    ]
    random.shuffle(gates)
    return gates

def new_game():
    p1_b, p2_b = make_bakugans()
    return {
        "p1_unused": p1_b, "p1_used": [],
        "p2_unused": p2_b, "p2_used": [],
        "p1_score": 0, "p2_score": 0,
        "p1_cards": make_cards(), "p2_cards": make_cards(),
        "gates": make_gates(),
        "round": 1,
        "current_gate": None,
        "b1": None,
        "b2": None,
    }

def recycle(player, gs):
    unused, used = f"{player}_unused", f"{player}_used"
    if not gs[unused] and gs[used]:
        random.shuffle(gs[used])
        gs[unused], gs[used] = gs[used], []

async def send_round_start(chat_id):
    gs = GAMES.get(chat_id)
    if not gs:
        return

    recycle("p1", gs)
    recycle("p2", gs)

    if not gs["p1_unused"] or not gs["p2_unused"] or not gs["gates"]:
        await end_game(chat_id)
        return

    gate = gs["gates"].pop(0)
    gs["current_gate"] = gate

    b1 = gs["p1_unused"].pop(0)
    b2 = gs["p2_unused"].pop(0)
    b1.reset()
    b2.reset()
    gs["b1"] = b1
    gs["b2"] = b2

    bonus1 = gate["bonuses"].get(b1.attribute, 0)
    bonus2 = gate["bonuses"].get(b2.attribute, 0)
    b1.current_g_power += bonus1
    b2.current_g_power += bonus2

    text = (
        f"⚔️ **РАУНД {gs['round']}**\n"
        f"💥 **Карта Ворот:** [ {gate['name']} ]\n\n"
        f"🟢 **Твой боец:** {b1.name} ({b1.attribute}) | Бонус: {bonus1:+d}G\n"
        f"🔴 **Боец соперника:** {b2.name} ({b2.attribute}) | Бонус: {bonus2:+d}G\n\n"
        f"⚡ **Текущие силы:** {b1.current_g_power}G vs {b2.current_g_power}G\n\n"
        f"Выбери карту способности для активации:"
    )

    buttons = []
    for card in gs["p1_cards"]:
        buttons.append([InlineKeyboardButton(text=f"{card.name} ({card.description})", callback_data=f"card_{card.id}")])
    buttons.append([InlineKeyboardButton(text="⏩ Пропустить ход (Пасс)", callback_data="card_pass")])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(chat_id, text, reply_markup=kb, parse_mode="Markdown")

async def end_game(chat_id):
    gs = GAMES.get(chat_id)
    p1 = gs["p1_score"]
    p2 = gs["p2_score"]

    if p1 > p2:
        res = "🎉 **ПОБЕДА! Ты величайший боец Вестрои!**"
    elif p2 > p1:
        res = "💀 **ПОРАЖЕНИЕ! Соперник захватил поле боя!**"
    else:
        res = "🤝 **Боевая ничья!**"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Играть снова", callback_data="start_new_game")]
    ])
    await bot.send_message(
        chat_id,
        f"🏁 **ИГРА ОКОНЧЕНА**\nИтог: Ты — {p1} | Соперник — {p2}\n\n{res}",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    GAMES.pop(chat_id, None)

# ---------- Обработчики Telegram ----------
@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 В бой!", callback_data="start_new_game")]
    ])
    await message.answer(
        "👋 Добро пожаловать на арену Бакуган!\nНажми кнопку ниже, чтобы начать дуэль против бота.",
        reply_markup=kb
    )

@dp.callback_query(F.data == "start_new_game")
async def handle_new_game(callback: CallbackQuery):
    await callback.answer()
    GAMES[callback.message.chat.id] = new_game()
    await callback.message.answer("🎲 Партии розданы! Бакуганы готовы к броску...")
    await send_round_start(callback.message.chat.id)

@dp.callback_query(F.data.startswith("card_"))
async def handle_card_choice(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    gs = GAMES.get(chat_id)
    if not gs:
        await callback.answer("Игра не найдена. Начни заново /start", show_alert=True)
        return

    await callback.answer()
    choice = callback.data.replace("card_", "")

    b1 = gs["b1"]
    b2 = gs["b2"]
    log_text = []

    # Ход игрока
    if choice != "pass":
        card = next((c for c in gs["p1_cards"] if c.id == choice), None)
        if card:
            gs["p1_cards"].remove(card)
            card.activate(b1, b2)
            log_text.append(f"✨ Ты активировал карту: **{card.name}**!")
    else:
        log_text.append("Ты решил не использовать способности.")

    # Ход бота (случайный выбор)
    if gs["p2_cards"] and random.choice([True, False]):
        bot_card = gs["p2_cards"].pop(random.randint(0, len(gs["p2_cards"]) - 1))
        bot_card.activate(b2, b1)
        log_text.append(f"🤖 Соперник активировал карту: **{bot_card.name}**!")
    else:
        log_text.append("Соперник не стал использовать карту.")

    # Итоги раунда
    log_text.append(f"\n📊 **Финальные силы:** {b1.name} ({b1.current_g_power}G) VS {b2.name} ({b2.current_g_power}G)")

    if b1.current_g_power > b2.current_g_power:
        gs["p1_score"] += 1
        log_text.append("🏆 Ты забираешь Карту Ворот!")
    elif b2.current_g_power > b1.current_g_power:
        gs["p2_score"] += 1
        log_text.append("💥 Соперник забирает Карту Ворот!")
    else:
        log_text.append("🤝 Ничья! Карта уходит в низ колоды.")
        gs["gates"].append(gs["current_gate"])

    gs["p1_used"].append(b1)
    gs["p2_used"].append(b2)
    gs["round"] += 1

    log_text.append(f"\nСчёт по картам: Ты — {gs['p1_score']} | Соперник — {gs['p2_score']}")

    await callback.message.edit_text("\n".join(log_text), parse_mode="Markdown")

    if gs["p1_score"] >= 3 or gs["p2_score"] >= 3 or gs["round"] > 30:
        await end_game(chat_id)
    else:
        await asyncio.sleep(2)
        await send_round_start(chat_id)

# ---------- Веб-сервер заглушка для Render ----------
async def health_check(request):
    return web.Response(text="Bot is running!", status=200)

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

async def main():
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
