# Customer Ticketing & Queue Management System

A lightweight **queue management system** built with **Flask** and **SQLite**, featuring:
- Ticket kiosks for customers
- Operator panels for staff
- Public display screens
- Optional ticket printing & audio announcements (Windows support)

---

## 🚀 Features
- **Kiosk Interface**: Customers select a service category and receive a ticket.
- **Operator Panel**: Staff call the next customer in their assigned category.
- **Display Screen**: Shows the most recently called tickets per category.
- **Text-to-Speech**: Announces called tickets aloud (via `pyttsx3`).
- **Printing Support**: Prints ticket slips on Windows (`win32print`).
- **Persistence**: All tickets are stored in a SQLite database.

---

## 🗂 Project Structure
customer_ticketing/
│── app.py # Main Flask entrypoint
│── config.py # Configuration (DB path, server IP, categories)
│── db.py # Database helpers (init, insert, update)
│── printer.py # Ticket printing (Windows only)
│── tts.py # Text-to-Speech announcements
│── routes/
│ ├── kiosk.py # Kiosk routes (/kiosk, /kiosk/take)
│ ├── operator.py # Operator routes (/operator/<counter>)
│ └── display.py # Display routes (/display, /api/status)
│── templates/
│ ├── kiosk.html # Kiosk UI
│ ├── operator.html # Operator UI
│ └── display.html # Display screen
│── queue.db # SQLite database (auto-created)


---

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/customer_ticketing.git
cd customer_ticketing
```

### 2. Create a virtual environment
```bash
python3 -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

If you don’t have requirements.txt yet, the main packages are:

```bash
pip install flask pyttsx3 pypiwin32
```
▶️ Usage
## 1. Run the server
```bash
python app.py
```

You’ll see:

Initializing database...
 * Running on http://127.0.0.1:5000

## 2. Open interfaces

Kiosk → http://127.0.0.1:5000/kiosk

Operator → http://127.0.0.1:5000/operator/1

Display → http://127.0.0.1:5000/display

## 3. Database inspection
```bash 
sqlite3 queue.db
sqlite> .tables
sqlite> SELECT * FROM tickets;
```
## 🖨️ Printing (Windows only)

Tickets are printed automatically via the default system printer (win32print).
On Linux/Mac, the app logs tickets to console instead.

## 🔊 Audio Announcements

Uses pyttsx3 to announce tickets being called:

“Ticket A101, please proceed to counter 1.”

## 🛠️ Development Notes

The project uses Flask Blueprints to keep routes modular.

Ticket counters are tracked both in memory and in the database.

On startup, the database is initialized automatically (init_db()).

Categories and counter mapping are configurable in config.py.

### 📝 TODO / Future Work

- [ ] **Server Restart Recovery**: Reload waiting tickets from the database into memory after a restart or power outage.  
- [ ] **Real-Time Updates**: Use WebSockets or Server-Sent Events to auto-refresh operator and display screens.  
- [ ] **Admin Dashboard**: View statistics, manage categories, and generate reports.  
- [ ] **Role-Based Access**: Authentication for admins vs operators.  
- [ ] **Deployment**: Add Dockerfile & docker-compose for easier setup.


 ### 👨‍💻 Author

Developed by [IAN WAHINYA](https://github.com/palmer-code),  
and [Stanley Murigi](https://github.com/StanleyMurigi).

