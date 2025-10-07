from flask import Blueprint, render_template, jsonify
import threading
from config import CATEGORIES
from db import add_ticket_to_db
from printer import print_ticket
import sqlite3
from config import DB

bp = Blueprint('kiosk', __name__)
ticket_counters = {}

def assign_counter_for_category(category_code):
    meta = CATEGORIES[category_code]
    eligible_counters = meta["counters"]
    counter_loads = {}
    for c in eligible_counters:
        counter_loads[c] = count_unserved_tickets_for_counter(c)
    min_counter = min(eligible_counters, key=lambda c: counter_loads[c])
    return min_counter

def count_unserved_tickets_for_counter(counter):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tickets WHERE counter=? AND status='waiting'", (counter,))
    count = c.fetchone()[0]
    conn.close()
    return count

@bp.route('/kiosk')
def kiosk():
    return render_template('kiosk.html', categories=CATEGORIES)

@bp.route('/kiosk/take/<prefix>', methods=['POST'])
def take_ticket(prefix):
    if prefix not in CATEGORIES:
        return jsonify({"ok": False, "error": "Invalid category"}), 400
    # Get the latest ticket number for this prefix from the DB
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT MAX(number) FROM tickets WHERE prefix=?", (prefix,))
    row = c.fetchone()
    last_num = row[0] if row and row[0] is not None else 100
    num = last_num + 1
    conn.close()
    counter = assign_counter_for_category(prefix)
    add_ticket_to_db(prefix, num, counter)
    threading.Thread(target=print_ticket, args=(prefix, num, counter), daemon=True).start()
    return jsonify({"ok": True, "ticket": f"{prefix}{num}", "counter": counter})

