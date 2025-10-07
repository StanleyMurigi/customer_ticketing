DB = 'queue.db'
SERVER_IP = '0.0.0.0'
PORT = 5000

CATEGORIES = {
    "G": {"label": "Sim Card registration",                  "default_counter": 3, "counters": [1, 3]}, #1/3 --3
    "S": {"label": "Mpesa or Sim Card Queries",      "default_counter": 1, "counters": [1, 2]}, #1/2/3--1
    "P": {"label": "Post Pay & Bill Payments",        "default_counter": 2, "counters": [1, 3]}, #1/2/3--2
    "B": {"label": "paybills/till services",     "default_counter": 1, "counters": [1, 3]}, #1/2---2
    "C": {"label": "Change of Ownership",    "default_counter": 1, "counters": [1, 2]}, #1/2---1
    "I": {"label": "Internet",               "default_counter": 3, "counters": [1, 3]}, #3
    "F": {"label": "Fraud",                  "default_counter": 2, "counters": [2]} #2
}



