import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pytz
import sys
import os

# Full list of room and announcement names with descriptions for parenthetical display
announcement_names = [
    "[Production] (For site-wide announcements)",  # Changed from FISHTANK.LIVE
    "FAMOUS HOUSE (For house-wide events like a tripped fire alarm, contestant elimination, challenge immunity, etc.)",
    "DEN", "LOUNGE", "LOCKER ROOM", "DECK", "YARD", "CATWALK", "MAIL ROOM",
    "KITCHEN", "ISLAND", "DINING ROOM", "HALLWAY", "B1", "B2", "B3", "VANITY",
    "PENTHOUSE", "LOFT", "JACUZZI", "BAR", "FLAT", "CONFESSIONAL"
]

# Variable to track if the timestamp is locked
timestamp_locked = False

# Function to remove leading zeroes from the hour if needed (universal workaround)
def format_time_without_leading_zeroes(time_str):
    return time_str.lstrip('0') if time_str.startswith('0') else time_str

# Get current time in EST with universal workaround
def get_current_time_est():
    est = pytz.timezone('US/Eastern')
    current_time_est = datetime.now(est)
    formatted_time = current_time_est.strftime("%I:%M%p")
    return format_time_without_leading_zeroes(formatted_time)

# Function to update the timestamp by incrementing or decrementing minutes with universal workaround
def adjust_timestamp(minutes):
    current_time = datetime.strptime(timestamp_var.get(), "%I:%M%p")
    new_time = current_time + timedelta(minutes=minutes)
    formatted_time = new_time.strftime("%I:%M%p")
    timestamp_var.set(format_time_without_leading_zeroes(formatted_time))

# Function to update the report
def generate_report():
    selected_announcement = announcement_var.get().split(' (')[0].upper()  # Extract main name and ensure uppercase
    timestamp = timestamp_var.get()
    message = message_content.get("1.0", "end-1c").strip()
    reporter_note = reporter_note_var.get().strip()

    # Validate that an announcement type is selected
    if selected_announcement == "ROOM/ANNOUNCEMENT":
        output_text.delete("1.0", "end")
        output_text.insert("1.0", "Please select a valid room/announcement type.")
        return

    # Check if reporter's note should be appended with a line break
    if reporter_note:
        reporter_note_formatted = f"\n*[Reporter's note: {reporter_note}]*"
    else:
        reporter_note_formatted = ""

    if selected_announcement and message:
        # Format the report based on the selected announcement type
        formatted_message = f"**{selected_announcement} // {timestamp}**: "
        
        # Italicize only the message part for special types
        if selected_announcement in ["[PRODUCTION]", "FAMOUS HOUSE"]:
            formatted_message += f"*{message}*"
        else:
            formatted_message += message
        
        formatted_message += reporter_note_formatted

        output_text.delete("1.0", "end")
        output_text.insert("1.0", formatted_message)
    else:
        output_text.delete("1.0", "end")
        output_text.insert("1.0", "Please enter a message.")

# Function to continuously update the timestamp every minute
def update_timestamp_continuously():
    if not timestamp_locked:
        timestamp_var.set(get_current_time_est())
    global update_job
    update_job = root.after(60000, update_timestamp_continuously)  # Schedule to run again in 60 seconds

# Function to lock or unlock the timestamp
def lock_timestamp():
    global timestamp_locked
    timestamp_locked = not timestamp_locked
    lock_button.config(text="Unlock Timestamp" if timestamp_locked else "Lock Timestamp")

# Function to copy report to clipboard
def copy_report():
    report = output_text.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(report)
    root.update()  # Ensures the clipboard is updated

# Function to handle window close event
def on_closing():
    # Cancel any scheduled `after()` calls
    if 'update_job' in globals():
        root.after_cancel(update_job)
    root.destroy()

# Initialize main window
root = tk.Tk()
root.title("Fishtank Live Report Creator")  # Set the window title

# Set the window icon (favicon) with PyInstaller compatibility
if getattr(sys, 'frozen', False):
    # The application is running as a bundled executable (e.g., created by PyInstaller)
    base_path = sys._MEIPASS
else:
    # The application is running in a normal Python environment
    base_path = os.path.abspath(".")

icon_path = os.path.join(base_path, 'app_icon.ico')
root.iconbitmap(icon_path)

# Allow window resizing only for specific rows and columns
root.rowconfigure(2, weight=1)  # Allow row with the message content to expand
root.rowconfigure(5, weight=1)  # Allow row with the output text box to expand
root.columnconfigure(1, weight=1)  # Allow the main column with the text boxes to expand

# Styling for padding and alignment
PAD_X = 10
PAD_Y = 5

# Dropdown for room and announcement selection
announcement_var = tk.StringVar(value="Room/Announcement")
announcement_label = tk.Label(root, text="Room/Announcement Type:")
announcement_label.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
announcement_menu = ttk.OptionMenu(root, announcement_var, "Room/Announcement", *announcement_names)
announcement_menu.grid(row=0, column=1, columnspan=4, padx=PAD_X, pady=PAD_Y, sticky="ew")

# Timestamp field
timestamp_label = tk.Label(root, text="Timestamp:")
timestamp_label.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
timestamp_var = tk.StringVar()
timestamp_var.set(get_current_time_est())
timestamp_entry = tk.Entry(root, textvariable=timestamp_var, justify="center", width=15)
timestamp_entry.grid(row=1, column=1, padx=(PAD_X, 2), pady=PAD_Y, sticky="w")

# Buttons to adjust timestamp with better alignment
timestamp_frame = tk.Frame(root)
timestamp_frame.grid(row=1, column=2, padx=(2, PAD_X), pady=PAD_Y, sticky="w")
timestamp_frame.columnconfigure(0, weight=0)  # Keep buttons fixed to the left
tk.Button(timestamp_frame, text="<<", command=lambda: adjust_timestamp(-1)).grid(row=0, column=0, padx=(0, 2), sticky="w")
tk.Button(timestamp_frame, text=">>", command=lambda: adjust_timestamp(1)).grid(row=0, column=1, padx=(2, 0), sticky="w")

# Lock timestamp button
lock_button = tk.Button(root, text="Lock Timestamp", command=lock_timestamp, width=15)
lock_button.grid(row=1, column=3, padx=(2, PAD_X), pady=PAD_Y, sticky="w")

# Message content input
message_label = tk.Label(root, text="Message:")
message_label.grid(row=2, column=0, padx=PAD_X, pady=PAD_Y, sticky="nw")
message_content = tk.Text(root, width=60, height=10)
message_content.grid(row=2, column=1, columnspan=4, padx=PAD_X, pady=PAD_Y, sticky="nsew")

# Reporter's note input
reporter_note_label = tk.Label(root, text="Reporter's Note (optional):")
reporter_note_label.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")
reporter_note_var = tk.StringVar()
reporter_note_entry = tk.Entry(root, textvariable=reporter_note_var, width=60)
reporter_note_entry.grid(row=3, column=1, columnspan=4, padx=PAD_X, pady=PAD_Y, sticky="ew")

# Button to generate the report
generate_button = tk.Button(root, text="Generate Report", command=generate_report)
generate_button.grid(row=4, column=0, columnspan=5, padx=PAD_X, pady=PAD_Y, sticky="ew")

# Label for generated report
output_label = tk.Label(root, text="Generated Report:")
output_label.grid(row=5, column=0, padx=PAD_X, pady=PAD_Y, sticky="w")

# Editable output text box with the same vertical space as the input
output_text = tk.Text(root, width=60, height=10, wrap="word")
output_text.grid(row=5, column=1, columnspan=4, padx=PAD_X, pady=PAD_Y, sticky="nsew")

# Button to copy report to clipboard
copy_button = tk.Button(root, text="Copy Report", command=copy_report)
copy_button.grid(row=6, column=0, columnspan=5, padx=PAD_X, pady=(PAD_Y, 20), sticky="ew")  # Added bottom padding for a "chin"

# Bind the window close event to the `on_closing` function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the continuous timestamp update
update_timestamp_continuously()

root.mainloop()
