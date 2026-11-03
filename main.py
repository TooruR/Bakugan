import os, asyncio, random, threading, uuid
from flask import Flask
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

TOKEN = os.getenv("BOTTOKEN", "8947362428:AAFMBUvYa_l3ThqiJrt24zKDOxxKjhZS9H8")
BOT_NAME = "bakugangame_bot"

web_app = Flask('')
@web_app.route('/')
def home(): return 'OK'
threading.Thread(target=lambda: web_app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080))), daemon=True).start()

bot, dp, router = Bot(token=TOKEN), Dispatcher(), Router()
dp.include_router(router)

ELEMS = {'Pyrus': '🔥 Пайрус', 'Aquos': '💧 Аквос', 'Haos': '⚡ Хаос', 'Ventus': '🍃 Вентус', 'Subterra': '🪨 Саптера', 'Darkus': '🌑 Даркус'}
ADV = {'Pyrus': 'Ventus', 'Ventus': 'Subterra', 'Subterra': 'Darkus', 'Darkus': 'Aquos', 'Aquos': 'Pyrus', 'Haos': 'Darkus'}

# 90 Бакуганов (по 15 на стихию): (Имя, Стихия, G)
RAW_B = [
    ("Dragonoid", "Pyrus", 340), ("Delta Dragonoid", "Pyrus", 450), ("Ultimate Dragonoid", "Pyrus", 550),
    ("Pyrus Griffon", "Pyrus", 330), ("Pyrus Falconeer", "Pyrus", 320), ("Pyrus Saurus", "Pyrus", 370),
    ("Pyrus Serpenoid", "Pyrus", 310), ("Pyrus Robotallion", "Pyrus", 350), ("Pyrus Mantris", "Pyrus", 390),
    ("Neo Dragonoid", "Pyrus", 400), ("Cross Dragonoid", "Pyrus", 600), ("Helix Dragonoid", "Pyrus", 650),
    ("Helios", "Pyrus", 460), ("Viper Helios", "Pyrus", 520), ("Cyborg Helios", "Pyrus", 620),
    ("Preyas", "Aquos", 340), ("Sirenoid", "Aquos", 370), ("Aquos Siege", "Aquos", 380),
    ("Aquos Limulus", "Aquos", 320), ("Aquos Juggernoid", "Aquos", 300), ("Aquos Robotallion", "Aquos", 340),
    ("Aquos Fear Ripper", "Aquos", 350), ("Aquos Saurus", "Aquos", 360), ("Preyas II", "Aquos", 430),
    ("Elfin", "Aquos", 400), ("Minx Elfin", "Aquos", 520), ("Elico", "Aquos", 500),
    ("Blast Elico", "Aquos", 600), ("Abis Omega", "Aquos", 420), ("Macubass", "Aquos", 620),
    ("Tigrerra", "Haos", 340), ("Blade Tigrerra", "Haos", 450), ("Tentaclear", "Haos", 370),
    ("Haos Hynoid", "Haos", 310), ("Haos Freezer", "Haos", 330), ("Haos Robotallion", "Haos", 350),
    ("Haos Falconeer", "Haos", 320), ("Haos Saurus", "Haos", 360), ("Nemus", "Haos", 450),
    ("Saint Nemus", "Haos", 550), ("Mega Brontes", "Haos", 480), ("Alto Brontes", "Haos", 560),
    ("Aranaut", "Haos", 500), ("Boriates", "Haos", 610), ("Dynamo", "Haos", 420),
    ("Skyress", "Ventus", 360), ("Storm Skyress", "Ventus", 450), ("Harpus", "Ventus", 370),
    ("Monarus", "Ventus", 330), ("Ventus Ravenoid", "Ventus", 350), ("Ventus Falconeer", "Ventus", 310),
    ("Ventus Griffon", "Ventus", 320), ("Ventus Robotallion", "Ventus", 340), ("Ingram", "Ventus", 460),
    ("Master Ingram", "Ventus", 540), ("Ventus Altair", "Ventus", 500), ("Wired", "Ventus", 410),
    ("Hawktor", "Ventus", 490), ("Strikeflier", "Ventus", 520), ("Aluze", "Ventus", 610),
    ("Gorem", "Subterra", 380), ("Hammer Gorem", "Subterra", 450), ("Subterra Cycloid", "Subterra", 370),
    ("Subterra Tuskor", "Subterra", 350), ("Subterra Wormquake", "Subterra", 320), ("Subterra Centipoid", "Subterra", 330),
    ("Subterra Saurus", "Subterra", 360), ("Clayf", "Subterra", 500), ("Wilda", "Subterra", 450),
    ("Magma Wilda", "Subterra", 560), ("Primo Vulcan", "Subterra", 480), ("Rex Vulcan", "Subterra", 580),
    ("Coredem", "Subterra", 510), ("Dryoid", "Subterra", 630), ("Scraper", "Subterra", 420),
    ("Hydranoid", "Darkus", 400), ("Dual Hydranoid", "Darkus", 480), ("Alpha Hydranoid", "Darkus", 550),
    ("Darkus Reaper", "Darkus", 370), ("Darkus Fear Ripper", "Darkus", 360), ("Darkus Mantris", "Darkus", 340),
    ("Darkus Centipoid", "Darkus", 330), ("Exedra", "Darkus", 500), ("Naga", "Darkus", 520),
    ("Percival", "Darkus", 470), ("Midnight Percival", "Darkus", 550), ("Linehalt", "Darkus", 500),
    ("Helios MK2", "Darkus", 670), ("Hades", "Darkus", 600), ("Farbros", "Darkus", 690)
]
BAKUGANS = [{'name': x[0], 'element': x[1], 'g': x[2]} for x in RAW_B]

GATES = [
    {'name': 'Зазеркалье Тьмы', 'elem': 'Darkus', 'g': 0, 'desc': 'Обмен силой'},
    {'name': 'Огненный Буст', 'elem': 'Pyrus', 'g': 250, 'desc': '+250 G Пайрусу'},
    {'name': 'Священный Свет', 'elem': 'Haos', 'g': 300, 'desc': '+300 G Хаосу'},
    {'name': 'Тайфун', 'elem': 'Ventus', 'g': 200, 'desc': '+200 G Вентусу'},
    {'name': 'Гравитация', 'elem': 'Subterra', 'g': 200, 'desc': '+200 G Саптере'},
    {'name': 'Арена Малой Силы', 'elem': 'Any', 'g': 0, 'desc': 'Инверсия'}
]

ABILS = [
    {'name': 'Огненный залп (+180 G)', 'elem': 'Pyrus', 'g': 180, 'h': 0},
    {'name': 'Водный Барьер (+150 G)', 'elem': 'Aquos', 'g': 150, 'h': 0},
    {'name': 'Лечение Океана (+150 HP)', 'elem': 'Aquos', 'g': 0, 'h': 150},
    {'name': 'Ослепляющий Свет (+160 G)', 'elem': 'Haos', 'g': 160, 'h': 0},
    {'name': 'Штормовой Всплеск (+200 G)', 'elem': 'Ventus', 'g': 200, 'h': 0},
    {'name': 'Каменный Панцирь (+220 G)', 'elem': 'Subterra', 'g': 220, 'h': 0},
    {'name': 'Теневой Коготь (+220 G)', 'elem': 'Darkus', 'g': 220, 'h': 0},
    {'name': 'Универсал (+120 G)', 'elem': 'Any', 'g': 120, 'h': 0}
]

class Player:
    def __init__(self, uid, name, is_bot=False):
        self.uid, self.name, self.is_bot = uid, name, is_bot
        self.hp, self.team, self.gates, self.abils = 1000, [], [], []
        self.d_elem, self.d_idx, self.stage = 'Pyrus', 0, 'baku'
        self.baku, self.gate, self.used_abils, self.gate_on = None, None, [], False
        self.done, self.act_text, self.mid = False, "", None

    def reset_round(self):
        self.baku, self.gate, self.used_abils, self.gate_on, self.done, self.act_text = None, None, [], False, False, ""

class Game:
    def __init__(self, rid, p1, is_bot=False):
        self.rid, self.p1, self.phase, self.step = rid, p1, 'draft', 1
        self.p2 = Player(0, "🤖 ИИ", True) if is_bot else None
        if is_bot:
            self.p2.team = random.sample(BAKUGANS, 3)
            self.p2.gates = random.sample(GATES, 3)
            self.p2.abils = random.sample(ABILS, 3)
            self.p2.stage = 'ready'

games, user_game = {}, {}

def get_g(p: Player, opp: Player):
    if not p.baku: return 0
    g = p.baku['g'] + sum(a['g'] for a in p.used_abils)
    if p.gate_on and p.gate:
        if p.gate['elem'] in (p.baku['element'], 'Any'): g += p.gate['g']
    if opp and opp.baku:
        if ADV.get(p.baku['element']) == opp.baku['element']: g += 150
        elif ADV.get(opp.baku['element']) == p.baku['element']: g -= 150
    return max(0, g)

async def upd(p: Player, txt, kb=None):
    if p.is_bot: return
    try:
        if p.mid: await bot.edit_message_text(txt, chat_id=p.uid, message_id=p.mid, reply_markup=kb, parse_mode="Markdown")
        else:
            m = await bot.send_message(p.uid, txt, reply_markup=kb, parse_mode="Markdown")
            p.mid = m.message_id
    except: pass

def draft_kb(p: Player):
    if p.stage == 'baku':
        cur = [b for b in BAKUGANS if b['element'] == p.d_elem]
        b = cur[p.d_idx % len(cur)]
        t = f"🛡️ *ВЫБОР БАКУГАНОВ ({len(p.team)}/3)*\n*{b['name']}* ({ELEMS[b['element']]}) — `{b['g']} G`"
        kb = [
            [InlineKeyboardButton(text=v[:1], callback_data=f"de_{k}") for k, v in ELEMS.items()],
            [InlineKeyboardButton(text="◀️", callback_data="dp"), InlineKeyboardButton(text="➕ Взять", callback_data="da"), InlineKeyboardButton(text="▶️", callback_data="dn")],
            [InlineKeyboardButton(text="🎲 3 Случайных", callback_data="dr")]
        ]
    elif p.stage == 'gate':
        c = GATES[p.d_idx % len(GATES)]
        t = f"🎴 *КАРТЫ ВОРОТ ({len(p.gates)}/3)*\n*{c['name']}* — _{c['desc']}_"
        kb = [[InlineKeyboardButton(text="◀️", callback_data="dp"), InlineKeyboardButton(text="➕ Взять", callback_data="da"), InlineKeyboardButton(text="▶️", callback_data="dn")], [InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")]]
    else:
        a = ABILS[p.d_idx % len(ABILS)]
        t = f"✨ *СПОСОБНОСТИ ({len(p.abils)}/3)*\n*{a['name']}*"
        kb = [[InlineKeyboardButton(text="◀️", callback_data="dp"), InlineKeyboardButton(text="➕ Взять", callback_data="da"), InlineKeyboardButton(text="▶️", callback_data="dn")], [InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")]]
    return t, InlineKeyboardMarkup(inline_keyboard=kb)

async def run_round(gm: Game):
    p1, p2 = gm.p1, gm.p2
    if gm.phase == 'gate':
        if p1.done and (p2.done or p2.is_bot):
            if p2.is_bot: p2.gate = p2.gates[0]
            gm.phase, p1.done, p2.done = 'baku', False, False
            for p in (p1, p2):
                if p.is_bot: continue
                kb = [[InlineKeyboardButton(text=f"{b['name']} ({b['g']}G)", callback_data=f"sb_{i}")] for i, b in enumerate(p.team)]
                await upd(p, "👾 *Брось бакугана взакрытую:*", InlineKeyboardMarkup(inline_keyboard=kb))
    elif gm.phase == 'baku':
        if p1.done and (p2.done or p2.is_bot):
            if p2.is_bot: p2.baku = random.choice(p2.team)
            gm.phase, gm.step, p1.done, p2.done = 'tactics', 1, False, False
            await next_step(gm)
    elif gm.phase == 'tactics':
        if p2.is_bot and not p2.done:
            if p2.abils: p2.used_abils.append(p2.abils.pop(0)); p2.act_text = "сыграл карту"
            else: p2.act_text = "пасс"
            p2.done = True
        if p1.done and p2.done:
            txt = f"⚡ *Шаг {gm.step}:*\n• {p1.name}: {p1.act_text}\n• {p2.name}: {p2.act_text}\n`{get_g(p1,p2)}G` VS `{get_g(p2,p1)}G`"
            if gm.step < 3:
                gm.step += 1; p1.done, p2.done = False, False
                for p in (p1, p2): await upd(p, txt)
                await next_step(gm)
            else:
                g1, g2 = get_g(p1, p2), get_g(p2, p1)
                dmg = min(500, max(250, abs(g1 - g2)))
                if g1 > g2: p2.hp = max(0, p2.hp - dmg); res = f"🏆 Раунд за {p1.name}! Урон: `{dmg}`"
                elif g2 > g1: p1.hp = max(0, p1.hp - dmg); res = f"🏆 Раунд за {p2.name}! Урон: `{dmg}`"
                else: res = "🤝 Ничья!"
                res += f"\n\n❤️ HP: {p1.name} `{p1.hp}` | {p2.name} `{p2.hp}`"
                if p1.hp <= 0 or p2.hp <= 0:
                    win = p1.name if p2.hp <= 0 else p2.name
                    for p in (p1, p2): await upd(p, f"{res}\n\n👑 *ПОБЕДИЛ {win}!*", InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
                    games.pop(gm.rid, None); return
                p1.reset_round(); p2.reset_round(); gm.phase = 'gate'
                for p in (p1, p2):
                    if p.is_bot: continue
                    kb = [[InlineKeyboardButton(text=g['name'], callback_data=f"sg_{i}")] for i, g in enumerate(p.gates)]
                    await upd(p, f"{res}\n\n🎴 *Новый раунд! Установи Ворота:*", InlineKeyboardMarkup(inline_keyboard=kb))

async def next_step(gm: Game):
    for p, opp in ((gm.p1, gm.p2), (gm.p2, gm.p1)):
        if p.is_bot: continue
        kb = [[InlineKeyboardButton(text=f"✨ {a['name']}", callback_data=f"sa_{i}")] for i, a in enumerate(p.abils)]
        if p.gate and not p.gate_on: kb.append([InlineKeyboardButton(text="💥 Открыть Ворота", callback_data="s_open")])
        kb.append([InlineKeyboardButton(text="⏩ Пасс", callback_data="s_pass")])
        await upd(p, f"⚔️ *Шаг {gm.step}/3*\nТы: `{get_g(p,opp)}G` | Враг: `{get_g(opp,p)}G`", InlineKeyboardMarkup(inline_keyboard=kb))

@router.message(CommandStart())
async def st(m: Message, command: CommandObject = None):
    args = command.args if command else None
    if args and args in games and not games[args].p2:
        gm = games[args]
        gm.p2 = Player(m.from_user.id, m.from_user.full_name)
        user_game[m.from_user.id] = args
        t, k = draft_kb(gm.p1); await upd(gm.p1, t, k)
        t, k = draft_kb(gm.p2); await upd(gm.p2, t, k)
        return
    kb = [[InlineKeyboardButton(text="⚔️ С Ботом", callback_data="m_bot")], [InlineKeyboardButton(text="👥 Создать PvP", callback_data="m_pvp")]]
    await m.answer("🔥 *АРЕНА БАКУГАН*", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

@router.callback_query(F.data.in_(["m_bot", "m_pvp", "menu"]))
async def cb_m(c: CallbackQuery):
    await c.answer()
    if c.data == "m_bot":
        rid = str(uuid.uuid4())[:8]
        gm = Game(rid, Player(c.from_user.id, c.from_user.full_name), True)
        games[rid] = gm; user_game[c.from_user.id] = rid
        t, k = draft_kb(gm.p1); await c.message.edit_text(t, reply_markup=k, parse_mode="Markdown")
    elif c.data == "m_pvp":
        rid = str(uuid.uuid4())[:6]
        gm = Game(rid, Player(c.from_user.id, c.from_user.full_name))
        games[rid] = gm; user_game[c.from_user.id] = rid
        await c.message.edit_text(f"👥 Ссылка для кента:\n`https://t.me/{BOT_NAME}?start={rid}`\nЖдем...", parse_mode="Markdown")
    else:
        kb = [[InlineKeyboardButton(text="⚔️ С Ботом", callback_data="m_bot")], [InlineKeyboardButton(text="👥 Создать PvP", callback_data="m_pvp")]]
        await c.message.edit_text("🔥 *АРЕНА БАКУГАН*", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

@router.callback_query(F.data.startswith("de_"))
async def cb_de(c: CallbackQuery):
    gm = games.get(user_game.get(c.from_user.id)); p = gm.p1 if gm.p1.uid == c.from_user.id else gm.p2
    p.d_elem, p.d_idx = c.data[3:], 0
    t, k = draft_kb(p); await c.message.edit_text(t, reply_markup=k, parse_mode="Markdown")

@router.callback_query(F.data.in_(["dp", "dn", "da", "dr"]))
async def cb_dnav(c: CallbackQuery):
    await c.answer()
    gm = games.get(user_game.get(c.from_user.id)); p = gm.p1 if gm.p1.uid == c.from_user.id else gm.p2
    if c.data == "dp": p.d_idx -= 1
    elif c.data == "dn": p.d_idx += 1
    elif c.data == "dr":
        if p.stage == 'baku': p.team = random.sample(BAKUGANS, 3); p.stage = 'gate'
        elif p.stage == 'gate': p.gates = random.sample(GATES, 3); p.stage = 'abil'
        else: p.abils = random.sample(ABILS, 3); p.stage = 'ready'
    elif c.data == "da":
        if p.stage == 'baku':
            cur = [b for b in BAKUGANS if b['element'] == p.d_elem]
            item = cur[p.d_idx % len(cur)]
            if item not in p.team: p.team.append(item)
            if len(p.team) >= 3: p.stage, p.d_idx = 'gate', 0
        elif p.stage == 'gate':
            item = GATES[p.d_idx % len(GATES)]
            if item not in p.gates: p.gates.append(item)
            if len(p.gates) >= 3: p.stage, p.d_idx = 'abil', 0
        elif p.stage == 'abil':
            item = ABILS[p.d_idx % len(ABILS)]
            if item not in p.abils: p.abils.append(item)
            if len(p.abils) >= 3: p.stage = 'ready'

    if p.stage == 'ready':
        opp = gm.p2 if gm.p1.uid == p.uid else gm.p1
        if opp.stage == 'ready' or opp.is_bot:
            gm.phase = 'gate'
            for pl in (gm.p1, gm.p2):
                if pl.is_bot: continue
                kb = [[InlineKeyboardButton(text=g['name'], callback_data=f"sg_{i}")] for i, g in enumerate(pl.gates)]
                await upd(pl, "🎴 *Установи Карту Ворот:*", InlineKeyboardMarkup(inline_keyboard=kb))
        else: await c.message.edit_text("⏳ Ждем соперника...")
    else:
        t, k = draft_kb(p); await c.message.edit_text(t, reply_markup=k, parse_mode="Markdown")

@router.callback_query(F.data.startswith("sg_"))
async def cb_sg(c: CallbackQuery):
    await c.answer()
    gm = games.get(user_game.get(c.from_user.id)); p = gm.p1 if gm.p1.uid == c.from_user.id else gm.p2
    p.gate = p.gates.pop(int(c.data[3:])); p.done = True
    await c.message.edit_text("🎴 Ворота установлены! Ждем врага...")
    await run_round(gm)

@router.callback_query(F.data.startswith("sb_"))
async def cb_sb(c: CallbackQuery):
    await c.answer()
    gm = games.get(user_game.get(c.from_user.id)); p = gm.p1 if gm.p1.uid == c.from_user.id else gm.p2
    p.baku = p.team[int(c.data[3:])]; p.done = True
    await c.message.edit_text(f"👾 Брошен *{p.baku['name']}*! Ждем...")
    await run_round(gm)

@router.callback_query(F.data.startswith("sa_"))
async def cb_sa(c: CallbackQuery):
    await c.answer()
    gm = games.get(user_game.get(c.from_user.id)); p = gm.p1 if gm.p1.uid == c.from_user.id else gm.p2
    a = p.abils.pop(int(c.data[3:]))
    p.used_abils.append(a); p.hp = min(1000, p.hp + a['h']); p.act_text = f"сыграл {a['name']}"; p.done = True
    await c.message.edit_text("✨ Карта сыграна! Ждем...")
    await run_round(gm)

@router.callback_query(F.data == "s_open")
async def cb_so(c: CallbackQuery):
    await c.answer()
    gm = games.get(user_game.get(c.from_user.id)); p = gm.p1 if gm.p1.uid == c.from_user.id else gm.p2
    p.gate_on, p.act_text, p.done = True, f"открыл {p.gate['name']}", True
    await c.message.edit_text("💥 Ворота открыты! Ждем...")
    await run_round(gm)

@router.callback_query(F.data == "s_pass")
async def cb_sp(c: CallbackQuery):
    await c.answer()
    gm = games.get(user_game.get(c.from_user.id)); p = gm.p1 if gm.p1.uid == c.from_user.id else gm.p2
    p.act_text, p.done = "пасс", True
    await c.message.edit_text("⏩ Пасс! Ждем...")
    await run_round(gm)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
