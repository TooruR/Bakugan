import os, asyncio, random, threading, uuid
from flask import Flask
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

TOKEN = os.getenv("BOTTOKEN", "8947362428:AAFMBUvYa_l3ThqiJrt24zKDOxxKjhZS9H8")
BOT_NAME = "bakugangame_bot"
NL = chr(10)

web_app = Flask('')
@web_app.route('/')
def home(): return 'OK'
threading.Thread(target=lambda: web_app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080))), daemon=True).start()

bot, dp, router = Bot(token=TOKEN), Dispatcher(), Router()
dp.include_router(router)

ELEMS = {'Pyrus': '🔥 Пайрус', 'Aquos': '💧 Аквос', 'Haos': '⚡ Хаос', 'Ventus': '🍃 Вентус', 'Subterra': '🪨 Саптера', 'Darkus': '🌑 Даркус'}
ADV = {'Pyrus': 'Ventus', 'Ventus': 'Subterra', 'Subterra': 'Darkus', 'Darkus': 'Aquos', 'Aquos': 'Pyrus', 'Haos': 'Darkus'}

RAW_B = [
("Dragonoid", "Pyrus", 340, "Сезон 1"), ("Delta Dragonoid", "Pyrus", 450, "Сезон 1"),
("Ultimate Dragonoid", "Pyrus", 550, "Сезон 1"), ("Pyrus Griffon", "Pyrus", 330, "Сезон 1"),
("Pyrus Falconeer", "Pyrus", 320, "Сезон 1"), ("Preyas", "Aquos", 340, "Сезон 1"),
("Sirenoid", "Aquos", 370, "Сезон 1"), ("Aquos Siege", "Aquos", 380, "Сезон 1"),
("Aquos Limulus", "Aquos", 320, "Сезон 1"), ("Aquos Juggernoid", "Aquos", 300, "Сезон 1"),
("Tigrerra", "Haos", 340, "Сезон 1"), ("Blade Tigrerra", "Haos", 450, "Сезон 1"),
("Tentaclear", "Haos", 370, "Сезон 1"), ("Haos Hynoid", "Haos", 310, "Сезон 1"),
("Haos Freezer", "Haos", 330, "Сезон 1"), ("Skyress", "Ventus", 360, "Сезон 1"),
("Storm Skyress", "Ventus", 450, "Сезон 1"), ("Harpus", "Ventus", 370, "Сезон 1"),
("Monarus", "Ventus", 330, "Сезон 1"), ("Ventus Ravenoid", "Ventus", 350, "Сезон 1"),
("Gorem", "Subterra", 380, "Сезон 1"), ("Hammer Gorem", "Subterra", 450, "Сезон 1"),
("Subterra Cycloid", "Subterra", 370, "Сезон 1"), ("Subterra Tuskor", "Subterra", 350, "Сезон 1"),
("Subterra Wormquake", "Subterra", 320, "Сезон 1"), ("Hydranoid", "Darkus", 400, "Сезон 1"),
("Dual Hydranoid", "Darkus", 480, "Сезон 1"), ("Alpha Hydranoid", "Darkus", 550, "Сезон 1"),
("Darkus Reaper", "Darkus", 370, "Сезон 1"), ("Darkus Fear Ripper", "Darkus", 360, "Сезон 1"),
("Neo Dragonoid", "Pyrus", 400, "Сезон 2"), ("Cross Dragonoid", "Pyrus", 600, "Сезон 2"),
("Helix Dragonoid", "Pyrus", 650, "Сезон 2"), ("Helios", "Pyrus", 460, "Сезон 2"),
("Viper Helios", "Pyrus", 520, "Сезон 2"), ("Preyas II", "Aquos", 430, "Сезон 2"),
("Elfin", "Aquos", 400, "Сезон 2"), ("Minx Elfin", "Aquos", 520, "Сезон 2"),
("Elico", "Aquos", 500, "Сезон 2"), ("Blast Elico", "Aquos", 600, "Сезон 2"),
("Nemus", "Haos", 450, "Сезон 2"), ("Saint Nemus", "Haos", 550, "Сезон 2"),
("Mega Brontes", "Haos", 480, "Сезон 2"), ("Alto Brontes", "Haos", 560, "Сезон 2"),
("Aranaut", "Haos", 500, "Сезон 2"), ("Ingram", "Ventus", 460, "Сезон 2"),
("Master Ingram", "Ventus", 540, "Сезон 2"), ("Ventus Altair", "Ventus", 500, "Сезон 2"),
("Wired", "Ventus", 410, "Сезон 2"), ("Hawktor", "Ventus", 490, "Сезон 2"),
("Wilda", "Subterra", 450, "Сезон 2"), ("Magma Wilda", "Subterra", 560, "Сезон 2"),
("Primo Vulcan", "Subterra", 480, "Сезон 2"), ("Rex Vulcan", "Subterra", 580, "Сезон 2"),
("Coredem", "Subterra", 510, "Сезон 2"), ("Percival", "Darkus", 470, "Сезон 2"),
("Midnight Percival", "Darkus", 550, "Сезон 2"), ("Linehalt", "Darkus", 500, "Сезон 2"),
("Helios MK2", "Darkus", 670, "Сезон 2"), ("Hades", "Darkus", 600, "Сезон 2"),
("Cyborg Helios", "Pyrus", 620, "Сезон 3"), ("Maxus Dragonoid", "Pyrus", 680, "Сезон 3"),
("Hyper Dragonoid", "Pyrus", 480, "Сезон 3"), ("Pyrus Verias", "Pyrus", 410, "Сезон 3"),
("Abis Omega", "Aquos", 420, "Сезон 3"), ("Macubass", "Aquos", 620, "Сезон 3"),
("Boriates", "Haos", 610, "Сезон 3"), ("Dynamo", "Haos", 420, "Сезон 3"),
("Strikeflier", "Ventus", 520, "Сезон 3"), ("Aluze", "Ventus", 610, "Сезон 3"),
("Dryoid", "Subterra", 630, "Сезон 3"), ("Scraper", "Subterra", 420, "Сезон 3"),
("Exedra", "Darkus", 500, "Сезон 3"), ("Naga", "Darkus", 520, "Сезон 3"),
("Farbros", "Darkus", 690, "Сезон 3")
]
BAKUGANS = [{'name': x[0], 'element': x[1], 'g': x[2], 'season': x[3]} for x in RAW_B]

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

QUIT_BTN = InlineKeyboardButton(text="🏳️ Выйти в меню", callback_data="quit")

def b_str(b):
return f"{b['name']} ({ELEMS[b['element']]}) [{b['season']}]"

class Player:
def __init__(self, uid, name, is_bot=False):
self.uid, https://www.google.com/url?q=http://self.name&source=gmail&ust=1793940488525000&sa=E, self.is_bot = uid, name, is_bot
self.hp, self.team, self.gates, self.abils = 1000, [], [], []
self.d_elem, self.d_idx, self.stage = 'Pyrus', 0, 'baku'
self.baku, self.gate, self.used_abils, self.gate_on = None, None, [], False
self.done, self.act_text, self.mid = False, "", None

def elems(self):
return {b['element'] for b in self.team} | {'Any'}

def valid_gates(self):
return [g for g in GATES if g['elem'] in self.elems()]

def valid_abils(self):
return [a for a in ABILS if a['elem'] in self.elems()]

def check_stage(self):
if len(self.team) < 3: self.stage = 'baku'
elif not self.gates: self.stage = 'gate'
elif not self.abils: self.stage = 'abil'
else: self.stage = 'ready'

def reset_round(self):
self.baku, self.gate, self.used_abils, self.gate_on, self.done, self.act_text = None, None, [], False, False, ""

class Game:
def __init__(self, rid, p1, is_bot=False):
self.rid, self.p1, self.phase, self.step = rid, p1, 'draft', 1
self.p2 = Player(0, "🤖 ИИ", True) if is_bot else None
if is_bot:
self.p2.team = random.sample(BAKUGANS, 3)
self.refill_bot()

def refill_bot(self):
if not self.p2.gates: self.p2.gates = random.sample(self.p2.valid_gates(), min(3, len(self.p2.valid_gates())))
if not self.p2.abils: self.p2.abils = random.sample(self.p2.valid_abils(), min(3, len(self.p2.valid_abils())))
self.p2.stage = 'ready'

games, user_game = {}, {}

def get_g(p: Player, opp: Player):
if not p.baku: return 0
g = p.baku['g'] + sum(a['g'] for a in p.used_abils)
if p.gate_on and p.gate and p.gate['elem'] in (p.baku['element'], 'Any'): g += p.gate['g']
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
lines = [f"• {b_str(x)} — `{x['g']} G`" for x in p.team]
team_block = "Твоя команда:" + NL + NL.join(lines) + NL + NL if lines else ""
t = f"🛡️ *НАБОР БАКУГАНОВ ({len(p.team)}/3)*" + NL + team_block + f"Боец: *{b_str(b)}*" + NL + f"Сила: `{b['g']} G`"
kb = [
[InlineKeyboardButton(text=v[:1], callback_data=f"de_{k}") for k, v in ELEMS.items()],
[InlineKeyboardButton(text="◀️", callback_data="dp"), InlineKeyboardButton(text="➕ Взять", callback_data="da"), InlineKeyboardButton(text="▶️", callback_data="dn")],
[InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")],
[QUIT_BTN]
]
elif p.stage == 'gate':
vg = p.valid_gates()
c = vg[p.d_idx % len(vg)]
t = f"🎴 *ДОБОР КАРТ ВОРОТ ({len(p.gates)}/3)*" + NL + "_(Под стихии твоих бойцов)_" + NL + NL + f"Карта: *{c['name']}* [{ELEMS.get(c['elem'], 'Универсальная')}]" + NL + f"Эффект: _{c['desc']}_"
kb = [[InlineKeyboardButton(text="◀️", callback_data="dp"), InlineKeyboardButton(text="➕ Взять", callback_data="da"), InlineKeyboardButton(text="▶️", callback_data="dn")], [InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")], [QUIT_BTN]]
else:
va = p.valid_abils()
a = va[p.d_idx % len(va)]
t = f"✨ *ДОБОР СПОСОБНОСТЕЙ ({len(p.abils)}/3)*" + NL + "_(Под стихии твоих бойцов)_" + NL + NL + f"Карта: *{a['name']}* [{ELEMS.get(a['elem'], 'Универсальная')}]" + NL + f"Описание: _{a['desc']}_"
kb = [[InlineKeyboardButton(text="◀️", callback_data="dp"), InlineKeyboardButton(text="➕ Взять", callback_data="da"), InlineKeyboardButton(text="▶️", callback_data="dn")], [InlineKeyboardButton(text="🎲 Случайно", callback_data="dr")], [QUIT_BTN]]
return t, InlineKeyboardMarkup(inline_keyboard=kb)

async def start_or_draft(gm: Game, prefix=""):
p1, p2 = gm.p1, gm.p2
if p2.is_bot: gm.refill_bot()
p1.check_stage(); p2.check_stage()

if p1.stage == 'ready' and p2.stage == 'ready':
gm.phase = 'gate'
for p in (p1, p2):
if p.is_bot: continue
kb = [[InlineKeyboardButton(text=f"{g['name']} ({g['desc']})", callback_data=f"sg_{i}")] for i, g in enumerate(p.gates)]
kb.append([QUIT_BTN])
await upd(p, f"{prefix}🎴 *Установи Карту Ворот взакрытую:*", InlineKeyboardMarkup(inline_keyboard=kb))
else:
gm.phase = 'draft'
for p in (p1, p2):
if p.is_bot: continue
if p.stage != 'ready':
t, k = draft_kb(p)
await upd(p, f"{prefix}🔄 *Нужен добор карт:*" + NL + NL + t, k)
else:
await upd(p, f"{prefix}⏳ Ждем, пока соперник наберет карты...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BTN]]))

async def run_round(gm: Game):
p1, p2 = gm.p1, gm.p2
if gm.phase == 'gate':
if p1.done and (p2.done or p2.is_bot):
if p2.is_bot: p2.gate = p2.gates.pop(0)
gm.phase, p1.done, p2.done = 'baku', False, False
for p in (p1, p2):
if p.is_bot: continue
kb = [[InlineKeyboardButton(text=f"{b_str(b)} — {b['g']} G", callback_data=f"sb_{i}")] for i, b in enumerate(p.team)]
kb.append([QUIT_BTN])
await upd(p, "👾 *Выбери и брось бакугана взакрытую:*", InlineKeyboardMarkup(inline_keyboard=kb))
elif gm.phase == 'baku':
if p1.done and (p2.done or p2.is_bot):
if p2.is_bot: p2.baku = random.choice(p2.team)
gm.phase, gm.step, p1.done, p2.done = 'tactics', 1, False, False
await next_step(gm)
elif gm.phase == 'tactics':
if p2.is_bot and not p2.done:
if p2.abils and random.choice([True, False]):
a = p2.abils.pop(0); p2.used_abils.append(a); p2.hp = min(1000, p2.hp + a['h']); p2.act_text = f"сыграл «{a['name']}» ({a['desc']})"
elif p2.gate and not p2.gate_on:
p2.gate_on = True; p2.act_text = f"открыл «{p2.gate['name']}» ({p2.gate['desc']})"
else: p2.act_text = "пропустил шаг"
p2.done = True
if p1.done and p2.done:
txt = f"⚡ *Итог шага {gm.step}:*" + NL + f"• {https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793940488525000&sa=E}: {p1.act_text}" + NL + f"• {https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793940488525000&sa=E}: {p2.act_text}" + NL + NL
if gm.step < 3:
gm.step += 1; p1.done, p2.done = False, False
await next_step(gm, txt)
else:
g1, g2 = get_g(p1, p2), get_g(p2, p1)
dmg = min(500, max(250, abs(g1 - g2)))
if g1 > g2: p2.hp = max(0, p2.hp - dmg); res = f"🏆 Раунд за {https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793940488525000&sa=E}! Урон: `{dmg}`"
elif g2 > g1: p1.hp = max(0, p1.hp - dmg); res = f"🏆 Раунд за {https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793940488525000&sa=E}! Урон: `{dmg}`"
else: res = "🤝 Ничья!"
res = txt + f"🏁 *Финал раунда ({g1}G vs {g2}G):* {res}" + NL + f"❤️ HP: {https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793940488525000&sa=E} `{p1.hp}` | {https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793940488525000&sa=E} `{p2.hp}`" + NL + NL
if p1.hp <= 0 or p2.hp <= 0:
win = https://www.google.com/url?q=http://p1.name&source=gmail&ust=1793940488525000&sa=E if p2.hp <= 0 else https://www.google.com/url?q=http://p2.name&source=gmail&ust=1793940488525000&sa=E
for p in (p1, p2): await upd(p, f"{res}👑 *ПОБЕДИЛ {win}!*", InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔄 В главное меню", callback_data="menu")]]))
games.pop(gm.rid, None); return
p1.reset_round(); p2.reset_round()
await start_or_draft(gm, res)

async def next_step(gm: Game, prefix=""):
for p, opp in ((gm.p1, gm.p2), (gm.p2, gm.p1)):
if p.is_bot: continue
kb = [[InlineKeyboardButton(text=f"✨ {a['name']} ({a['desc']})", callback_data=f"sa_{i}")] for i, a in enumerate(p.abils)]
if p.gate and not p.gate_on: kb.append([InlineKeyboardButton(text=f"💥 Открыть Ворота: {p.gate['name']}", callback_data="s_open")])
kb.append([InlineKeyboardButton(text="⏩ Пропустить шаг (Пасс)", callback_data="s_pass")])
kb.append([QUIT_BTN])
info = prefix + f"⚔️ *ТАКТИЧЕСКИЙ БОЙ (Шаг {gm.step}/3)*" + NL + f"🟢 Ты ({https://www.google.com/url?q=http://p.name&source=gmail&ust=1793940488525000&sa=E}) — HP: `{p.hp}`" + NL + f"Боец: *{b_str(p.baku)}* | Сила: `{get_g(p,opp)} G`" + NL + NL + f"🔴 Враг ({https://www.google.com/url?q=http://opp.name&source=gmail&ust=1793940488525000&sa=E}) — HP: `{opp.hp}`" + NL + f"Боец: *{b_str(opp.baku)}* | Сила: `{get_g(opp,p)} G`"
await upd(p, info, InlineKeyboardMarkup(inline_keyboard=kb))

@router.message(CommandStart())
async def st(m: Message, command: CommandObject = None):
args = command.args if command else None
if args and args in games and not games[args].p2:
gm = games[args]
gm.p2 = Player(https://www.google.com/url?q=http://m.from_user.id&source=gmail&ust=1793940488525000&sa=E, m.from_user.full_name)
user_game[https://www.google.com/url?q=http://m.from_user.id&source=gmail&ust=1793940488525000&sa=E] = args
t, k = draft_kb(gm.p1); await upd(gm.p1, t, k)
t, k = draft_kb(gm.p2); await upd(gm.p2, t, k)
return
kb = [[InlineKeyboardButton(text="⚔️ Играть с Ботом", callback_data="m_bot")], [InlineKeyboardButton(text="👥 Играть с кентом (PvP)", callback_data="m_pvp")]]
await m.answer("🔥 *АРЕНА БАКУГАН: ГЛАВНОЕ МЕНЮ*", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

@router.callback_query(F.data == "quit")
async def cb_quit(c: CallbackQuery):
await c.answer("Вы вышли из матча")
rid = user_game.pop(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E, None)
if rid and rid in games:
gm = games.pop(rid)
opp = gm.p2 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E else gm.p1
if opp and not opp.is_bot:
user_game.pop(opp.uid, None)
kb = [[InlineKeyboardButton(text="🔄 В меню", callback_data="menu")]]
await upd(opp, "🏳️ *Соперник покинул игру! Победа за тобой!*", InlineKeyboardMarkup(inline_keyboard=kb))
kb = [[InlineKeyboardButton(text="⚔️ Играть с Ботом", callback_data="m_bot")], [InlineKeyboardButton(text="👥 Играть с кентом (PvP)", callback_data="m_pvp")]]
await c.message.edit_text("🔥 *АРЕНА БАКУГАН: ГЛАВНОЕ МЕНЮ*", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

@router.callback_query(F.data.in_(["m_bot", "m_pvp", "menu"]))
async def cb_m(c: CallbackQuery):
await c.answer()
if c.data == "m_bot":
rid = str(uuid.uuid4())[:8]
gm = Game(rid, Player(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E, c.from_user.full_name), True)
games[rid] = gm; user_game[https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E] = rid
gm.p1.mid = c.message.message_id
t, k = draft_kb(gm.p1); await upd(gm.p1, t, k)
elif c.data == "m_pvp":
rid = str(uuid.uuid4())[:6]
gm = Game(rid, Player(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E, c.from_user.full_name))
games[rid] = gm; user_game[https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E] = rid
gm.p1.mid = c.message.message_id
await c.message.edit_text(f"👥 *Комната создана!*" + NL + f"Перешли код кенту: `{rid}`" + NL + f"Или напиши ему ввести: `/start {rid}`" + NL + NL + "⏳ Ждем подключения...", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[QUIT_BTN]]), parse_mode="Markdown")
else:
kb = [[InlineKeyboardButton(text="⚔️ Играть с Ботом", callback_data="m_bot")], [InlineKeyboardButton(text="👥 Играть с кентом (PvP)", callback_data="m_pvp")]]
await c.message.edit_text("🔥 *АРЕНА БАКУГАН: ГЛАВНОЕ МЕНЮ*", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

@router.callback_query(F.data.startswith("de_"))
async def cb_de(c: CallbackQuery):
gm = games.get(user_game.get(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E))
if not gm: return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488525000&sa=E else gm.p2
p.d_elem, p.d_idx = c.data[3:], 0
t, k = draft_kb(p); await upd(p, t, k)

@router.callback_query(F.data.in_(["dp", "dn", "da", "dr"]))
async def cb_dnav(c: CallbackQuery):
await c.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E))
if not gm: return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E else gm.p2
if c.data == "dp": p.d_idx -= 1
elif c.data == "dn": p.d_idx += 1
elif c.data == "dr":
if p.stage == 'baku': p.team = random.sample(BAKUGANS, 3)
elif p.stage == 'gate': p.gates = random.sample(p.valid_gates(), min(3, len(p.valid_gates())))
elif p.stage == 'abil': p.abils = random.sample(p.valid_abils(), min(3, len(p.valid_abils())))
p.d_idx = 0; p.check_stage()
elif c.data == "da":
if p.stage == 'baku':
cur = [b for b in BAKUGANS if b['element'] == p.d_elem]
item = cur[p.d_idx % len(cur)]
if item not in p.team: p.team.append(item)
if len(p.team) >= 3: p.d_idx = 0; p.check_stage()
elif p.stage == 'gate':
vg = p.valid_gates()
item = vg[p.d_idx % len(vg)]
if item not in p.gates: p.gates.append(item)
if len(p.gates) >= 3: p.d_idx = 0; p.check_stage()
elif p.stage == 'abil':
va = p.valid_abils()
item = va[p.d_idx % len(va)]
if item not in p.abils: p.abils.append(item)
if len(p.abils) >= 3: p.d_idx = 0; p.check_stage()

if p.stage == 'ready':
await start_or_draft(gm)
else:
t, k = draft_kb(p); await upd(p, t, k)

@router.callback_query(F.data.startswith("sg_"))
async def cb_sg(c: CallbackQuery):
await c.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E))
if not gm: return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E else gm.p2
p.gate = p.gates.pop(int(c.data[3:])); p.done = True
await upd(p, "🎴 Ворота установлены! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BTN]]))
await run_round(gm)

@router.callback_query(F.data.startswith("sb_"))
async def cb_sb(c: CallbackQuery):
await c.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E))
if not gm: return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E else gm.p2
p.baku = p.team[int(c.data[3:])]; p.done = True
await upd(p, f"👾 Брошен *{b_str(p.baku)}*! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BTN]]))
await run_round(gm)

@router.callback_query(F.data.startswith("sa_"))
async def cb_sa(c: CallbackQuery):
await c.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E))
if not gm: return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E else gm.p2
a = p.abils.pop(int(c.data[3:]))
p.used_abils.append(a); p.hp = min(1000, p.hp + a['h']); p.act_text = f"сыграл «{a['name']}» ({a['desc']})"; p.done = True
await upd(p, "✨ Карта сыграна! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BTN]]))
await run_round(gm)

@router.callback_query(F.data == "s_open")
async def cb_so(c: CallbackQuery):
await c.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E))
if not gm: return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E else gm.p2
p.gate_on, p.act_text, p.done = True, f"открыл «{p.gate['name']}» ({p.gate['desc']})", True
await upd(p, "💥 Ворота открыты! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BTN]]))
await run_round(gm)

@router.callback_query(F.data == "s_pass")
async def cb_sp(c: CallbackQuery):
await c.answer()
gm = games.get(user_game.get(https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E))
if not gm: return
p = gm.p1 if gm.p1.uid == https://www.google.com/url?q=http://c.from_user.id&source=gmail&ust=1793940488526000&sa=E else gm.p2
p.act_text, p.done = "пропустил шаг", True
await upd(p, "⏩ Пасс! Ждем соперника...", InlineKeyboardMarkup(inline_keyboard=[[QUIT_BTN]]))
await run_round(gm)

async def main():
await bot.delete_webhook(drop_pending_updates=True)
await dp.start_polling(bot)

if __name__ == '__main__':
asyncio.run(main())
