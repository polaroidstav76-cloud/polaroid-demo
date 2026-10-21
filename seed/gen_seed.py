"""Выдуманные данные для демо-копии сайта. Запуск: python3 seed/gen_seed.py <папка import> <папка вывода>.
Справочник берётся из карточек (import/<slug>/kartochka.json), всё остальное придумано."""
import json, random, sys, uuid, os, datetime as dt
from pathlib import Path

random.seed(76)
IMPORT = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
MSK = dt.timezone(dt.timedelta(hours=3))
TODAY = dt.date(2026, 10, 21)
NOW = dt.datetime(2026, 10, 21, 9, 0, tzinfo=MSK)
def ts(d): return d.astimezone(dt.timezone.utc).isoformat()
def serial(d): return (d - dt.date(1899, 12, 30)).days
out = {}

# --- Справочник
products = []
for i, f in enumerate(sorted(IMPORT.glob('*/kartochka.json'))):
    k = json.load(open(f))
    products.append({'id': str(uuid.UUID(int=random.getrandbits(128), version=4)), 'name': k['name'], 'sku': k.get('sku') or '',
                     'category': k.get('category') or 'Прочее', 'description': json.dumps(k.get('description_blocks') or [], ensure_ascii=False),
                     'tags': [], 'image_url': None, 'sort_order': None})
out['products'] = products
pid = {p['name']: p['id'] for p in products}

# --- Филиалы, сотрудники
out['sales_branches'] = [
    {'id': 1, 'name': 'Филиал на Ленина', 'is_active': True, 'is_test': False, 'is_workshop': False},
    {'id': 2, 'name': 'ТЦ «Радуга»', 'is_active': True, 'is_test': False, 'is_workshop': False},
    {'id': 3, 'name': 'Мастерская', 'is_active': True, 'is_test': False, 'is_workshop': True},
    {'id': 4, 'name': 'Тестовый филиал', 'is_active': True, 'is_test': True, 'is_workshop': False}]
people = ['Анна Смирнова', 'Мария Котова', 'Дарья Белова', 'Ольга Новикова', 'Ксения Орлова', 'Екатерина Лебедева']
out['sales_people'] = [{'id': i + 1, 'name': n, 'is_active': True, 'retouch_lead_default': i == 0} for i, n in enumerate(people)]
emps, eid = [], {}
for p in range(1, 7):
    for b in (1, 2, 4):
        e = len(emps) + 1; eid[(p, b)] = e
        emps.append({'id': e, 'branch_id': b, 'name': people[p - 1], 'is_active': True, 'person_id': p})
out['sales_employees'] = emps
out['sales_pay_rates'] = [{'employee_id': eid[(p, b)], 'branch_id': b, 'shift_rate': 2000 if b == 1 else 2200, 'retouch_rate': 100, 'is_active': True}
                          for p in range(1, 7) for b in (1, 2)]

# --- Каталог кассы
CAT = [
    ('Фотопечать', 'product', 'Фото 10х15', '005', 25), ('Фотопечать', 'product', 'Фото 15х21 (А5)', '012', 60),
    ('Фотопечать', 'product', 'Фото 21х30 (А4)', '010', 120), ('Фотопечать', 'product', 'Фото 30х40', '030', 350),
    ('Фотопечать', 'product', 'Фото в стиле Полароид', '371', 40), ('Фотопечать', 'product', 'Фото 10х15 двустороннее', '404', 45),
    ('Услуги', 'service', 'Фото на документы', '003', 350), ('Услуги', 'service', 'Ретушь фото', '044', 200),
    ('Услуги', 'service', 'Сканирование', '061', 50), ('Услуги', 'service', 'Ламинирование А4', '066', 100),
    ('Услуги', 'service', 'Переплет', '301', 250), ('Услуги', 'service', 'Макет', '077', 300),
    ('Сувениры', 'product', 'Кружка с фото', '025', 550), ('Сувениры', 'product', 'Подарочная упаковка', '026', 200),
    ('Сувениры', 'product', 'Фотомагнит', '189', 150), ('Сувениры', 'product', 'Брелок акриловый', '345', 300),
    ('Сувениры', 'product', 'Пазл с фото А4', '437', 600), ('Сувениры', 'product', 'Подушка с фото', '439', 1200),
    ('Сувениры', 'product', 'Футболка с принтом', '436', 1500), ('Сувениры', 'product', 'Звёздная карта', '510', 1800),
    ('Сувениры', 'product', 'Бокал с гравировкой', '127', 900), ('Сувениры', 'product', 'Ручка с логотипом', '428', 250),
    ('Полиграфия', 'product', 'Визитки 100 шт', '150', 900), ('Полиграфия', 'product', 'Флаеры А6 100 шт', '151', 1500),
    ('Полиграфия', 'product', 'Стикеры круглые, лист', '152', 300), ('Полиграфия', 'product', 'Самоклейка А4', '080', 150),
    ('Широкоформатная печать', 'product', 'Холст 30х40', '200', 1900), ('Широкоформатная печать', 'product', 'Холст 40х60', '201', 2900),
    ('Широкоформатная печать', 'product', 'Баннер 1 м²', '0002', 700), ('Широкоформатная печать', 'product', 'Фото 50х70', '202', 900),
    ('Офис', 'service', 'Печать ч/б А4', '100', 10), ('Офис', 'service', 'Печать цветная А4', '101', 30),
    ('Офис', 'service', 'Ксерокопия', '102', 10),
    ('Календари и блокноты', 'product', 'Календарь настенный', '300', 1200), ('Календари и блокноты', 'product', 'Блокнот с фото', '086', 450),
    ('Календари и блокноты', 'product', 'Открытка-книга', '310', 350),
    ('Товары', 'product', 'Рамка 10х15', '400', 250), ('Товары', 'product', 'Рамка 21х30', '401', 450),
    ('Товары', 'product', 'Фотоальбом', '402', 900), ('Товары', 'product', 'Подарочный пакет', '403', 100)]
catalog = []
for i, (cat, t, name, sku, price) in enumerate(CAT, 1):
    whole = [{'min_qty': 50, 'price': round(price * 0.8)}, {'min_qty': 200, 'price': round(price * 0.65)}] if name.startswith('Фото 1') else []
    catalog.append({'id': i, 'item_type': t, 'name': name, 'sku': sku, 'price': price, 'is_active': True, 'cost_price': round(price * 0.38),
                    'category': cat, 'comment': None, 'wholesale_prices': whole, 'image_url': None})
out['sales_catalog'] = catalog
cid = {c['name']: c['id'] for c in catalog}
price = {c['id']: c['price'] for c in catalog}
out['sales_upsell_rules'] = [
    {'source_catalog_id': cid['Кружка с фото'], 'suggested_catalog_id': cid['Подарочная упаковка'], 'min_quantity': 1, 'max_quantity': None,
     'question': 'Предложить подарочную упаковку с открыткой и бантом?', 'is_active': True},
    {'source_catalog_id': cid['Фото 10х15'], 'suggested_catalog_id': cid['Рамка 10х15'], 'min_quantity': 1, 'max_quantity': 3,
     'question': 'Предложить рамку для фото?', 'is_active': True},
    {'source_catalog_id': cid['Фото 21х30 (А4)'], 'suggested_catalog_id': cid['Рамка 21х30'], 'min_quantity': 1, 'max_quantity': None,
     'question': 'Предложить рамку А4?', 'is_active': True},
    {'source_catalog_id': cid['Фото 10х15'], 'suggested_catalog_id': cid['Фотоальбом'], 'min_quantity': 30, 'max_quantity': None,
     'question': 'Много фото: предложить фотоальбом?', 'is_active': True}]

# --- Склад
MAT = [  # id, name, unit, min, code, workshop, pack_qty, pack_price
    (1, 'Фотобумага 10х15 глянец', 'лист', 300, 'FB-1015', False, 500, 1650),
    (2, 'Фотобумага А4 глянец', 'лист', 60, 'FB-A4', False, 50, 780),
    (3, 'Фотобумага А5', 'лист', 60, 'FB-A5', False, 100, 900),
    (4, 'Кружка-заготовка белая', 'шт', 12, 'KR-330', False, 36, 3600),
    (5, 'Коробка для кружки', 'шт', 10, 'KR-BOX', False, 50, 1500),
    (6, 'Магнитный винил А4', 'лист', 10, 'MV-A4', False, 10, 900),
    (7, 'Офисная бумага А4', 'лист', 500, 'OF-A4', False, 500, 450),
    (8, 'Плёнка для ламинирования А4', 'шт', 50, 'LM-A4', False, 100, 700),
    (9, 'Холст в рулоне', 'м', 5, 'HL-ROLL', True, 30, 9000),
    (10, 'Подрамник 30х40', 'шт', 5, 'PD-3040', True, 10, 2500),
    (11, 'Подрамник 40х60', 'шт', 5, 'PD-4060', True, 10, 3800),
    (12, 'Футболка белая', 'шт', 5, 'FT-WH', True, 10, 3500),
    (17, 'Рамка 10х15', 'шт', 10, 'RM-1015', False, 20, 2400),
    (18, 'Рамка 21х30', 'шт', 6, 'RM-A4', False, 10, 2200),
    (19, 'Пакет подарочный', 'шт', 20, 'PK-01', False, 50, 1500)]
mats = []
for (i, n, u, mn, code, ws, pq, pp) in MAT:
    mats.append({'id': i, 'name': n, 'unit': u, 'min_qty': mn, 'comment': None, 'is_active': True, 'purchase_code': code, 'in_workshop': ws,
                 'pack_qty': pq, 'pack_price': pp, 'per_sale_qty': 0, 'variant_catalog_id': None, 'no_track': False, 'parent_id': None,
                 'var_size': None, 'var_color': None, 'var_sizes': ['S', 'M', 'L', 'XL'] if i == 12 else [], 'var_colors': [],
                 'store_branch_id': None, 'archived': False})
for j, s in enumerate(['S', 'M', 'L', 'XL']):
    mats.append({'id': 13 + j, 'name': 'Футболка белая ' + s, 'unit': 'шт', 'min_qty': 5, 'comment': None, 'is_active': True, 'purchase_code': 'FT-WH',
                 'in_workshop': True, 'pack_qty': 10, 'pack_price': 3500, 'per_sale_qty': 0, 'variant_catalog_id': None, 'no_track': False,
                 'parent_id': 12, 'var_size': s, 'var_color': None, 'var_sizes': [], 'var_colors': [], 'store_branch_id': None, 'archived': False})
out['stock_materials'] = mats
NORMS = [('Фото 10х15', 1, 1), ('Фото в стиле Полароид', 1, 1), ('Фото 10х15 двустороннее', 1, 1), ('Фото 15х21 (А5)', 3, 1),
         ('Фото 21х30 (А4)', 2, 1), ('Фото на документы', 1, 1), ('Кружка с фото', 4, 1), ('Подарочная упаковка', 5, 1),
         ('Фотомагнит', 6, 0.125), ('Печать ч/б А4', 7, 1), ('Печать цветная А4', 7, 1), ('Ксерокопия', 7, 1),
         ('Ламинирование А4', 8, 1), ('Холст 30х40', 9, 0.4), ('Холст 30х40', 10, 1), ('Холст 40х60', 9, 0.7), ('Холст 40х60', 11, 1),
         ('Футболка с принтом', 12, 1), ('Рамка 10х15', 17, 1), ('Рамка 21х30', 18, 1), ('Подарочный пакет', 19, 1)]
out['stock_norms'] = [{'id': i, 'catalog_id': cid[c], 'material_id': m, 'qty': q, 'active': True, 'per_line': False} for i, (c, m, q) in enumerate(NORMS, 1)]
moves = []
start = dt.datetime.combine(TODAY - dt.timedelta(days=26), dt.time(10), MSK)
for m in mats:
    if m['var_sizes']: continue
    brs = [3] if m['in_workshop'] else [1, 2]
    for b in brs:
        q = (m['pack_qty'] or 10) * (3 if m['id'] in (1, 7) else 2)
        moves.append({'material_id': m['id'], 'branch_id': b, 'qty': q, 'kind': 'receipt', 'group_id': str(uuid.UUID(int=random.getrandbits(128), version=4)),
                      'price_total': (m['pack_price'] or 0) * q / (m['pack_qty'] or 1), 'supplier': 'ООО «ФотоОпт»', 'comment': 'Начальный остаток',
                      'person_name': 'Администратор', 'created_at': ts(start)})
out['stock_moves'] = moves
out['stock_requests'] = [
    {'id': 1, 'branch_id': 1, 'person_name': 'Мария Котова', 'name': 'Скотч двусторонний', 'qty': 3, 'comment': 'для рамок', 'status': 'open', 'created_at': ts(NOW - dt.timedelta(days=1))},
    {'id': 2, 'branch_id': 2, 'person_name': 'Дарья Белова', 'name': 'Картридж для ч/б принтера', 'qty': 1, 'comment': None, 'status': 'open', 'created_at': ts(NOW - dt.timedelta(days=2))}]

# --- Клиенты (выдуманные)
FN = ['Алексей', 'Ирина', 'Сергей', 'Наталья', 'Дмитрий', 'Елена', 'Павел', 'Юлия', 'Андрей', 'Светлана', 'Максим', 'Татьяна', 'Игорь', 'Виктория', 'Роман',
      'Полина', 'Артём', 'Алина', 'Кирилл', 'Вера', 'Никита', 'Людмила', 'Глеб', 'Софья', 'Олег']
LN = ['И.', 'К.', 'П.', 'С.', 'М.', 'Л.', 'Т.', 'Р.', 'Б.', 'Г.']
custs = []
for i, n in enumerate(FN):
    custs.append({'id': str(uuid.UUID(int=random.getrandbits(128), version=4)), 'name': n + ' ' + random.choice(LN) + ' (демо)',
                  'phone': '7900000%04d' % (i + 11), 'comment': random.choice([None, None, 'постоянный клиент', 'любит матовую бумагу']),
                  'created_at': ts(NOW - dt.timedelta(days=random.randint(30, 200))), 'created_by_employee_id': random.randint(1, 6)})
out['loyalty_customers'] = custs
out['loyalty_gift_rules'] = [{'id': 1, 'order_count': 5, 'gift_name': 'Магнит с фото'}, {'id': 2, 'order_count': 10, 'gift_name': 'Кружка с фото'}]

# --- Смены и продажи за 24 дня
shifts, sse, sales, items, pays, rets, ltx = [], [], [], [], [], [], []
order_no = {1: 1000, 2: 5000}
staff_of = {1: [1, 2, 3], 2: [4, 5, 6]}
WEIGHTS = [('Фото 10х15', 30), ('Фото 15х21 (А5)', 8), ('Фото 21х30 (А4)', 8), ('Фото на документы', 12), ('Печать ч/б А4', 12), ('Печать цветная А4', 8),
           ('Ксерокопия', 8), ('Кружка с фото', 6), ('Подарочная упаковка', 3), ('Фотомагнит', 5), ('Ретушь фото', 5), ('Сканирование', 4),
           ('Ламинирование А4', 4), ('Холст 30х40', 2), ('Холст 40х60', 1), ('Фото в стиле Полароид', 5), ('Рамка 10х15', 3), ('Рамка 21х30', 2),
           ('Визитки 100 шт', 1), ('Флаеры А6 100 шт', 1), ('Календарь настенный', 1), ('Пазл с фото А4', 1), ('Брелок акриловый', 2),
           ('Футболка с принтом', 1), ('Переплет', 2), ('Подарочный пакет', 2), ('Самоклейка А4', 2), ('Фото 30х40', 1)]
names, wts = zip(*WEIGHTS)
PM = [('cash', 25), ('card', 40), ('qr', 18), ('transfer', 10), ('link', 4), ('bank_account', 3)]
sid = saleid = itemid = 0
for days_ago in range(24, 0, -1):
    day = TODAY - dt.timedelta(days=days_ago)
    for b in (1, 2):
        if b == 2 and day.weekday() == 0: continue
        sid += 1
        team = random.sample(staff_of[b], 2 if day.weekday() >= 4 else 1)
        st = dt.datetime.combine(day, dt.time(9, random.randint(0, 20)), MSK); en = dt.datetime.combine(day, dt.time(20, random.randint(0, 30)), MSK)
        shifts.append({'id': sid, 'branch_id': b, 'employee_id': eid[(team[0], b)], 'started_at': ts(st), 'ended_at': ts(en), 'status': 'closed', 'no_pay': False})
        for k, p in enumerate(team):
            sse.append({'shift_id': sid, 'employee_id': eid[(p, b)], 'is_lead': k == 0, 'created_at': ts(st)})
        n = random.randint(14, 30) if day.weekday() >= 4 else random.randint(8, 20)
        for _ in range(n):
            saleid += 1; order_no[b] += 1
            at = st + dt.timedelta(minutes=random.randint(5, int((en - st).total_seconds() // 60) - 5))
            lines = []
            for nm in set(random.choices(names, wts, k=random.choice([1, 1, 1, 2, 2, 3]))):
                q = random.choice([1, 2, 4, 10, 20]) if nm in ('Фото 10х15', 'Печать ч/б А4', 'Ксерокопия', 'Фото в стиле Полароид') else random.choice([1, 1, 1, 2])
                if nm == 'Фото на документы': q = 1
                lines.append((cid[nm], nm, q))
            gross = sum(price[c] * q for c, _, q in lines)
            disc = random.choice([0] * 12 + [5, 10])
            dam = round(gross * disc / 100, 2); total = round(gross - dam, 2)
            pm = random.choices([m for m, _ in PM], [w for _, w in PM])[0]
            cust = random.choice(custs)['id'] if (pm == 'bank_account' or random.random() < 0.18) else None
            emp = eid[(random.choice(team), b)]
            sales.append({'id': saleid, 'shift_id': sid, 'branch_id': b, 'employee_id': emp, 'payment_method': pm, 'total': total, 'comment': None,
                          'status': 'completed', 'created_at': ts(at), 'gross_total': gross, 'loyalty_points_used': 0, 'loyalty_customer_id': cust,
                          'receipt_issued': True, 'order_number': order_no[b], 'discount_percent': disc, 'discount_amount': dam,
                          'payment_status': 'paid', 'paid_at': ts(at)})
            for c, nm, q in lines:
                itemid += 1
                items.append({'id': itemid, 'sale_id': saleid, 'catalog_id': c, 'item_type': next(x['item_type'] for x in catalog if x['id'] == c),
                              'item_name': nm, 'quantity': q, 'unit_price': price[c], 'line_total': price[c] * q,
                              'cost_price': round(price[c] * 0.38), 'cost_total': round(price[c] * 0.38) * q,
                              'variant_material_id': 13 + random.randint(0, 3) if nm == 'Футболка с принтом' else None})
            pays.append({'sale_id': saleid, 'payment_method': pm, 'amount': total, 'created_at': ts(at)})
            if cust:
                ltx.append({'customer_id': cust, 'transaction_type': 'purchase', 'order_amount': gross, 'points': round(gross * 0.05, 2),
                            'comment': None, 'available_at': ts(at + dt.timedelta(hours=24)), 'created_at': ts(at)})
        if random.random() < 0.12:
            s = random.choice([x for x in sales if x['shift_id'] == sid])
            s['status'] = 'returned'; s['returned_at'] = s['created_at']
            rets.append({'sale_id': s['id'], 'shift_id': sid, 'branch_id': b, 'employee_id': s['employee_id'], 'amount': s['total'],
                         'comment': 'Клиенту не понравилась цветопередача, перепечатали', 'created_at': s['created_at']})
out['sales_shifts'] = shifts; out['sales_shift_employees'] = sse; out['sales'] = sales; out['sale_items'] = items
out['sale_payments'] = pays; out['sales_returns'] = rets; out['loyalty_transactions'] = ltx
out['sales_branch_order_counters'] = [{'branch_id': 1, 'next_number': order_no[1] + 1}, {'branch_id': 2, 'next_number': order_no[2] + 1},
                                      {'branch_id': 4, 'next_number': 9000}]
out['pickup_orders'] = [
    {'branch_id': 1, 'shift_id': shifts[-2]['id'], 'employee_id': eid[(2, 1)], 'order_number': order_no[1] + 1,
     'items': [{'catalog_id': cid['Холст 40х60'], 'name': 'Холст 40х60', 'item_type': 'product', 'quantity': 1, 'unit_price': 2900, 'line_total': 2900, 'variant_material_id': None}],
     'gross_total': 2900, 'discount_percent': 0, 'total': 2900, 'client_name': 'Telegram @demo_client', 'client_phone': None,
     'comment': 'Заберёт в субботу', 'status': 'pending', 'created_at': ts(NOW - dt.timedelta(days=1, hours=3)), 'client_order_ref': 'Холст с семейным фото'},
    {'branch_id': 2, 'shift_id': shifts[-1]['id'], 'employee_id': eid[(5, 2)], 'order_number': order_no[2] + 1,
     'items': [{'catalog_id': cid['Календарь настенный'], 'name': 'Календарь настенный', 'item_type': 'product', 'quantity': 3, 'unit_price': 1200, 'line_total': 3600, 'variant_material_id': None}],
     'gross_total': 3600, 'discount_percent': 10, 'total': 3240, 'client_name': None, 'client_phone': '+79000000099',
     'comment': 'Корпоративный заказ', 'status': 'pending', 'created_at': ts(NOW - dt.timedelta(days=4)), 'client_order_ref': None}]
for o in out['pickup_orders']: pass
out['sales_branch_order_counters'][0]['next_number'] += 1; out['sales_branch_order_counters'][1]['next_number'] += 1

# --- Задания, объявления, чеки
out['sales_shift_tasks'] = [{'branch_id': b, 'task_date': str(TODAY), 'title': 'Протереть витрину и проверить ценники', 'description': None, 'is_active': True} for b in (1, 2)]
out['sales_person_tasks'] = [{'person_id': 2, 'title': 'Пройти тест по кружкам', 'description': 'Раздел «Справочник» → Кружка → Пройти тест', 'start_date': str(TODAY - dt.timedelta(days=2)), 'is_active': True}]
out['announcements'] = [
    {'title': 'Новая услуга: звёздная карта', 'body': 'Теперь делаем звёздные карты. Инструкция в справочнике, цена в кассе.', 'is_active': True, 'created_at': ts(NOW - dt.timedelta(days=6))},
    {'title': 'Подорожала печать 30х40', 'body': 'С понедельника фото 30х40 стоит 350 ₽.', 'is_active': True, 'created_at': ts(NOW - dt.timedelta(days=3))}]
out['branch_checks'] = [
    {'branch_id': 1, 'check_date': str(TODAY - dt.timedelta(days=1)), 'order_no': str(order_no[1] - 3), 'product': 'Холст 30х40', 'payment': 'Оплачено картой',
     'deadline': 'К пятнице', 'contacts': 'Telegram @demo_client', 'readiness': 'В работе'},
    {'branch_id': 2, 'check_date': str(TODAY - dt.timedelta(days=2)), 'order_no': str(order_no[2] - 5), 'product': 'Визитки 100 шт', 'payment': 'Предоплата 50%',
     'deadline': 'Завтра', 'contacts': '+7 900 000-00-21', 'readiness': 'Готово'}]

# --- Шаблоны сообщений
out['message_templates'] = [
    {'title': 'Приветствие', 'category': 'Общие', 'sort_order': 1, 'body': 'Здравствуйте! Спасибо, что обратились в фотоцентр. Пришлите, пожалуйста, фото и размер — я рассчитаю стоимость.'},
    {'title': 'Заказ готов', 'category': 'Общие', 'sort_order': 2, 'body': 'Ваш заказ готов! Забрать можно ежедневно с 9:00 до 20:00. Адрес: ул. Ленина, 1 (демо).'},
    {'title': 'Требования к файлам', 'category': 'Печать', 'sort_order': 3, 'body': 'Для качественной печати присылайте файлы в JPG или PDF, разрешение от 300 dpi, без сжатия в мессенджере (лучше файлом).'},
    {'title': 'Кружка: сроки', 'category': 'Сувениры', 'sort_order': 4, 'body': 'Кружку с вашим фото сделаем за 1 день. Предлагаем подарочную упаковку с открыткой и бантом — 200 ₽.'},
    {'title': 'Холст: макет', 'category': 'Широкоформат', 'sort_order': 5, 'body': 'Перед печатью холста пришлём макет на согласование. Срок изготовления — 2 дня.'},
    {'title': 'Доставка', 'category': 'Общие', 'sort_order': 6, 'body': 'Можем отправить заказ курьером по городу, стоимость от 300 ₽. Напишите адрес и удобное время.'}]

# --- Обучение
tq = []
for i, (q, a, cat) in enumerate([
        ('Сколько стоит фото 10х15?', '25 рублей', 'Фотопечать'), ('Какой объём у кружки?', '330 мл', 'Сувениры'),
        ('В каком формате лучше присылать файлы?', 'JPG или PDF', 'Печать'), ('Сколько делается холст?', '2 дня', 'Широкоформат'),
        ('Что обязательно предлагаем к кружке?', 'Подарочную упаковку', 'Сувениры'), ('Какое разрешение нужно для печати?', '300 dpi', 'Печать')], 1):
    tq.append({'test_id': 1, 'question_text': q, 'correct_answer': a, 'category': cat, 'sort_order': i})
out['tests'] = [{'id': 1, 'title': 'Тест для стажёра', 'description': 'Базовые вопросы по услугам фотоцентра', 'is_active': True}]
out['test_questions'] = tq
gq = []
for name, qs in [('Кружка', [('Какой объём у кружки?', ['250 мл', '330 мл', '500 мл'], 1), ('Можно ли нанести принт на кружку клиента?', ['Да', 'Нет, только на нашу заготовку'], 1)]),
                 ('Фото 10х15', [('Сколько стоит фото 10х15?', ['15 ₽', '25 ₽', '40 ₽'], 1)]),
                 ('Холст', [('Нужно ли согласовывать макет холста?', ['Да', 'Нет'], 0)])]:
    if name in pid:
        for i, (q, o, c) in enumerate(qs):
            gq.append({'product_id': pid[name], 'question': q, 'options': o, 'correct_index': c, 'sort_order': i})
out['guide_questions'] = gq

# --- Калькуляторы
out['sheet_print_price_rules'] = [{'sheet_width_cm': 32, 'sheet_height_cm': 45, 'sides': s, 'min_sheets': m, 'retail_price': r, 'wholesale_price': w, 'material_name': 'Мелованная 300 г'}
                                  for s, m, r, w in [('single', 1, 120, 100), ('single', 10, 90, 75), ('single', 50, 70, 60), ('double', 1, 180, 150), ('double', 10, 140, 120), ('double', 50, 110, 95)]]
out['sheet_lamination_price_rules'] = [{'material_name': 'Мелованная 300 г', 'sheet_width_cm': 32, 'sheet_height_cm': 45, 'min_sheets': m, 'retail_price': r, 'wholesale_price': w, 'sides': s}
                                       for s, m, r, w in [('single', 1, 60, 50), ('single', 10, 45, 40), ('double', 1, 100, 85), ('double', 10, 80, 70)]]
out['sheet_service_price_rules'] = [{'sheet_width_cm': 32, 'sheet_height_cm': 45, 'service_type': t, 'min_sheets': m, 'retail_price': r, 'wholesale_price': w}
                                    for t, m, r, w in [('cutting', 1, 50, 40), ('cutting', 10, 30, 25), ('different_images', 1, 20, 15)]]
out['shirt_print_price_rules'] = [{'scope': 'own', 'rule_type': 'base', 'print_type': None, 'size_type': None, 'min_qty': 1, 'retail_price': 700, 'wholesale_price': 550}] + \
    [{'scope': sc, 'rule_type': 'print', 'print_type': pt, 'size_type': sz, 'min_qty': mq, 'retail_price': r, 'wholesale_price': w}
     for sc, pt, sz, mq, r, w in [('own', 'dtf', '1', 1, 800, 650), ('own', 'dtf', '0.5', 1, 500, 400), ('client', 'dtf', '1', 1, 900, 750),
                                  ('client', 'dtf', '0.5', 1, 600, 500), ('own', 'film', '1', 1, 700, 550), ('client', 'film', '1', 1, 800, 650)]]
out['plotter_film_prices'] = [{'color': c, 'sheet_width_cm': 50, 'sheet_length_cm': 100, 'price': p} for c, p in [('Белая', 600), ('Чёрная', 600), ('Золото', 900), ('Серебро', 900)]]

# --- График
out['schedule_columns'] = [{'id': 1, 'title': 'Ленина', 'branch_id': 1, 'sort_order': 1, 'slots': 2, 'need_weekday': 1, 'need_weekend': 2, 'is_active': True},
                           {'id': 2, 'title': 'Радуга', 'branch_id': 2, 'sort_order': 2, 'slots': 2, 'need_weekday': 1, 'need_weekend': 2, 'is_active': True}]
colors = ['#FDE68A', '#BFDBFE', '#C7D2FE', '#FBCFE8', '#BBF7D0', '#FED7AA']
out['schedule_rules'] = [{'person_id': p, 'in_schedule': True, 'color': colors[p - 1], 'days': [], 'column_ids': [1 if p <= 3 else 2], 'helper_column_ids': [],
                          'target_shifts': 15, 'max_in_row': 3, 'note': None, 'min_in_row': None, 'max_off_row': None, 'helper_only_column_ids': []} for p in range(1, 7)]
out['schedule_months'] = [{'month': '2026-10-01', 'published': True}, {'month': '2026-11-01', 'published': False}]
cells = []
d = dt.date(2026, 10, 1)
while d < dt.date(2026, 12, 1):
    for col, ppl in ((1, [1, 2, 3]), (2, [4, 5, 6])):
        k = d.toordinal()
        cells.append({'work_date': str(d), 'column_id': col, 'slot': 1, 'person_id': ppl[k % 3]})
        if d.weekday() >= 4: cells.append({'work_date': str(d), 'column_id': col, 'slot': 2, 'person_id': ppl[(k + 1) % 3]})
    d += dt.timedelta(days=1)
out['schedule_cells'] = cells
out['schedule_requests'] = [{'person_id': 3, 'date_from': '2026-11-10', 'date_to': '2026-11-12', 'note': 'Сессия в университете', 'is_active': True}]

# --- Общий отчет: лист на каждый филиал, месяцы август–декабрь 2026
HEAD = ['Дата', 'День недели', 'Смена', 'Выручка', 'Курьер', 'Расходы', 'Карта', 'QR', 'Ссылка', 'Перевод', 'Р/с', 'Чеков', 'Возвраты',
        'Наличные в кассе', 'Инкассация', 'Прочие расходы', 'Ретушь', 'Комментарий', 'Зарплата']
WD = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
COLS = [chr(65 + i) for i in range(19)]
def daysales(b, day):
    ss = [s for s in sales if s['branch_id'] == b and s['status'] == 'completed' and dt.datetime.fromisoformat(s['created_at']).astimezone(MSK).date() == day]
    return ss
sheets = []
for b, title in ((1, 'Ленина выручка'), (2, 'Радуга выручка')):
    rows, months, r = {}, [], 1
    for mon in range(8, 13):
        first = dt.date(2026, mon, 1); last = (dt.date(2026, mon + 1, 1) if mon < 12 else dt.date(2027, 1, 1)) - dt.timedelta(days=1)
        hr = r; rows[str(hr)] = {c: {'s': 0, 'v': h} for c, h in zip(COLS, HEAD)}; r += 1
        f = r; dd = first
        while dd <= last:
            row = {'A': {'v': serial(dd)}, 'B': {'v': WD[dd.weekday()]}}
            if dd < TODAY:
                ss = daysales(b, dd)
                if ss or dd < TODAY - dt.timedelta(days=24):
                    base = sum(s['total'] for s in ss) if ss else random.randint(9000, 26000)
                    cnt = len(ss) if ss else random.randint(15, 45)
                    def pm(m): return sum(s['total'] for s in ss if s['payment_method'] == m) if ss else round(base * {'card': .4, 'qr': .2, 'transfer': .1}.get(m, 0))
                    who = '/'.join(sorted({people[e['person_id'] - 1].split()[0] for s in ss for e in emps if e['id'] == s['employee_id']})) if ss else random.choice(['Анна', 'Мария', 'Дарья'] if b == 1 else ['Ольга', 'Ксения', 'Екатерина'])
                    row.update({'C': {'v': who}, 'D': {'v': base}, 'E': {'v': random.choice([0, 0, 300])}, 'F': {'v': random.choice([0, 0, 450, 800])},
                                'G': {'v': pm('card')}, 'H': {'v': pm('qr')}, 'I': {'v': pm('link')}, 'J': {'v': pm('transfer')}, 'K': {'v': pm('bank_account')},
                                'L': {'v': cnt}, 'M': {'v': 0}, 'N': {'v': random.randint(1500, 6000)}, 'O': {'v': 0}, 'P': {'v': random.choice([0, 0, 250])},
                                'Q': {'v': random.randint(0, 4)}, 'S': {'v': 2000 if b == 1 else 2200}})
            rows[str(r)] = row; r += 1; dd += dt.timedelta(days=1)
        t = r
        rows[str(t)] = {'A': {'s': 1, 'v': 'Итого'}, **{c: {'s': 1, 'f': f'SUM({c}{f}:{c}{t - 1})', 'v': sum((rows[str(i)].get(c, {}).get('v') or 0) for i in range(f, t) if isinstance(rows[str(i)].get(c, {}).get('v'), (int, float)))}
                                                       for c in 'DEFGHIJKLMNOPQS'}}
        months.append({'m': f'2026-{mon:02d}', 'from': hr, 'to': t}); r += 2
    sheets.append({'sort_order': b * 10, 'title': title, 'branch_id': b, 'staff_visible': False, 'months': months,
                   'data': {'ncols': 19, 'cols': {c: 12 for c in COLS} | {'R': 30}, 'styles': [{'b': 1, 'bg': 'FFFF00'}, {'b': 1, 'bg': 'BDD7EE'}],
                            'merges': [], 'heights': {}, 'rows': rows}})
plan = {'1': {c: {'s': 0, 'v': h} for c, h in zip('ABCDE', ['Что купить', 'Где', 'Количество', 'Цена', 'Статус'])},
        '2': {'A': {'v': 'Фотобумага 10х15'}, 'B': {'v': 'ФотоОпт'}, 'C': {'v': 4}, 'D': {'v': 1650}, 'E': {'v': 'заказано'}},
        '3': {'A': {'v': 'Кружки-заготовки'}, 'B': {'v': 'СувенирПром'}, 'C': {'v': 2}, 'D': {'v': 3600}, 'E': {'v': 'нужно купить'}},
        '4': {'A': {'v': 'Плёнка для ламинирования'}, 'B': {'v': 'Офис-маркет'}, 'C': {'v': 1}, 'D': {'v': 700}, 'E': {'v': 'куплено'}}}
sheets.append({'sort_order': 90, 'title': 'Закупка', 'branch_id': None, 'staff_visible': True, 'months': [],
               'data': {'ncols': 5, 'cols': {'A': 30, 'B': 18, 'C': 12, 'D': 12, 'E': 16}, 'styles': [{'b': 1, 'bg': 'FFFF00'}], 'merges': [], 'heights': {}, 'rows': plan}})
out['report_sheets'] = sheets

for k, v in out.items():
    json.dump(v, open(OUT / f'{k}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print({k: len(v) for k, v in out.items()})
print('bytes', sum(os.path.getsize(OUT / f'{k}.json') for k in out))
