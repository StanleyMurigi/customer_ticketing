from flask import Blueprint, render_template, jsonify
from config import CATEGORIES
from db import mark_served_in_db, get_unserved_tickets_for_counter, get_next_ticket_for_counter
from tts import tts_say

bp = Blueprint('operator', __name__, url_prefix="/operator")

current_serving = {}  # counter_number: (prefix, num)

@bp.route('/<int:counter>')
def operator(counter):
    return render_template('operator.html', counter=counter, categories=CATEGORIES)

@bp.route('/<int:counter>/call', methods=['POST'])
def call_next(counter):
    # Get the oldest unserved ticket for this counter from the DB
    ticket = get_next_ticket_for_counter(counter)
    if not ticket:
        return jsonify({"ok": False, "message": "No tickets"}), 200

    prefix, num = ticket
    mark_served_in_db(prefix, num)
    announce_text = f"Ticket {prefix}{num}, please proceed to counter {counter}"
    tts_say(announce_text)
    current_serving[counter] = (prefix, num)
    return jsonify({"ok": True, "ticket": f"{prefix}{num}", "counter": counter, "announce": announce_text})

@bp.route('/<int:counter>/new_tickets')
def new_tickets(counter):
    # Get all unserved tickets for this counter from the DB, sorted by created_at
    tickets = get_unserved_tickets_for_counter(counter)
    ticket_strings = [f"{prefix}{num}" for prefix, num, _ in tickets]
    return jsonify(ticket_strings)

@bp.route('/display/current')
def display_current():
    # Only show counters 1, 2, 3
    result = {}
    for counter in [1, 2, 3]:
        if counter in current_serving:
            prefix, num = current_serving[counter]
            result[counter] = f"{prefix}{num}"
        else:
            result[counter] = "-"
    return jsonify(result)
