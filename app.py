import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

entries = []

# --- Logic ---
def time_to_minutes(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m


def minutes_to_time(minutes):
    sign = "-" if minutes < 0 else ""
    minutes = abs(minutes)
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


def calculate(operation):
    try:
        values = []
        for e in entries:
            val = e.get()
            if val:
                h, m = map(int, val.split(':'))
                if m > 59:
                    raise ValueError("Minutes must be <= 59")
                values.append(time_to_minutes(val))

        if not values:
            raise ValueError("Add at least one time value")

        result = values[0]
        for v in values[1:]:
            result = result + v if operation == "add" else result - v

        result_label.configure(text=minutes_to_time(result))
    except Exception as e:
        messagebox.showerror("Error", str(e))


# --- Navigation ---
def focus_up(event, current):
    idx = entries.index(current)
    if idx > 0:
        entries[idx - 1].focus()


def focus_down(event, current):
    idx = entries.index(current)
    if idx < len(entries) - 1:
        entries[idx + 1].focus()


# --- Input behavior ---
def validate_and_style(entry, formatted):
    try:
        if len(formatted) == 5:
            h, m = map(int, formatted.split(':'))
            if m > 59:
                entry.configure(border_color="red")
                return False
        entry.configure(border_color="#3b82f6")
        return True
    except:
        entry.configure(border_color="red")
        return False


def on_key_release(event, entry):
    raw = entry.get().replace(":", "")
    raw = ''.join([c for c in raw if c.isdigit()])[:4]

    # auto format
    if len(raw) >= 3:
        formatted = raw[:2] + ":" + raw[2:]
    else:
        formatted = raw

    entry.delete(0, "end")
    entry.insert(0, formatted)

    validate_and_style(entry, formatted)

    # auto jump
    if len(formatted) == 5:
        focus_down(None, entry)

    # delete behavior
    if event.keysym == "BackSpace" and formatted == "":
        if len(entries) > 1:
            idx = entries.index(entry)
            entry.destroy()
            entries.remove(entry)
            if idx > 0:
                entries[idx - 1].focus()


def on_enter(event, entry):
    new_entry = add_input()
    new_entry.focus()

def on_shift(event, entry):
    raw = entry.get().replace(":", "")
    raw = ''.join([c for c in raw if c.isdigit()])[:2]

    if raw:
        formatted = raw.zfill(2) + ":"
        entry.delete(0, "end")
        entry.insert(0, formatted)

def add_input():
    entry = ctk.CTkEntry(scroll_frame, placeholder_text="HH:MM", width=250, height=40, corner_radius=12)
    entry.pack(pady=6)

    entry.bind("<Up>", lambda e, ent=entry: focus_up(e, ent))
    entry.bind("<Down>", lambda e, ent=entry: focus_down(e, ent))
    entry.bind("<KeyRelease>", lambda e, ent=entry: on_key_release(e, ent))
    entry.bind("<Return>", lambda e, ent=entry: on_enter(e, ent))
    entry.bind("<Shift_L>", lambda e, ent=entry: on_shift(e, ent))
    entry.bind("<Shift_R>", lambda e, ent=entry: on_shift(e, ent))

    entries.append(entry)
    return entry


def clear_all():
    for e in entries:
        e.destroy()
    entries.clear()
    result_label.configure(text="00:00")


# --- GUI ---
app = ctk.CTk()
app.title("Time Calculator")
app.geometry("420x520")

# Title
title = ctk.CTkLabel(app, text="Time Calculator", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(pady=15)

# Scrollable frame
scroll_frame = ctk.CTkScrollableFrame(app, width=300, height=250, corner_radius=15)
scroll_frame.pack(pady=10)

# Initial inputs
for _ in range(2):
    add_input()

# Buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

add_btn = ctk.CTkButton(btn_frame, text="+ Add", fg_color="#22c55e", hover_color="#16a34a",
                        command=lambda: calculate("add"), width=120, corner_radius=10)
add_btn.grid(row=0, column=0, padx=5, pady=5)

sub_btn = ctk.CTkButton(btn_frame, text="- Subtract", fg_color="#ef4444", hover_color="#dc2626",
                        command=lambda: calculate("subtract"), width=120, corner_radius=10)
sub_btn.grid(row=0, column=1, padx=5, pady=5)

more_btn = ctk.CTkButton(btn_frame, text="+ Input", command=add_input, width=120, corner_radius=10)
more_btn.grid(row=1, column=0, padx=5, pady=5)

clear_btn = ctk.CTkButton(btn_frame, text="Clear", fg_color="#64748b", hover_color="#475569",
                          command=clear_all, width=120, corner_radius=10)
clear_btn.grid(row=1, column=1, padx=5, pady=5)

# Result
result_label = ctk.CTkLabel(app, text="00:00", font=ctk.CTkFont(size=28, weight="bold"))
result_label.pack(pady=20)

app.mainloop()
