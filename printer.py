import time, platform

if platform.system() == 'Windows':
    import win32print

def print_ticket(prefix, number, counter):
    # Construct ticket data with ESC/POS commands
    ticket_data = (
        b'\x1b\x40'  # Initialize printer
        + b'\x1b\x61\x01'  # Center alignment
        + b'\x1b\x45\x01'  # Bold ON
        + "CUSTOMER SERVICE CENTER\n".encode('ascii')
        + "WELCOME TO SAFARICOM TWO RIVERS MALL\n".encode('ascii')
        + b'\x1b\x45\x00'  # Bold OFF
        + b"-------------------------\n"
        + b'\x1b\x61\x00'  # Align left
        + b'\x1b\x45\x01'  # Bold ON
        + f"Ticket No: {prefix}{number}\n".encode('ascii')
        + f"Counter: {counter}\n".encode('ascii')
        + b'\x1b\x45\x00'  # Bold OFF
        + f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n".encode('ascii')
        + b"-------------------------\n"
        + b"Please wait for your number to be called.\n"
        # Add an extra newline and more feed lines
        + b'\n'
        + b'\x1b\x64\x05'  # Feed 5 lines for clean cut spacing
        # Auto cut
        + b'\x1d\x56\x00'  # Full cut
    )

    try:
        printer_name = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, ticket_data)
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
    except Exception as e:
        print("Printing error:", e)
