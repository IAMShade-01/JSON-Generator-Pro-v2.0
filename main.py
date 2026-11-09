import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os
import sys
import zipfile
import logging
import getpass
from datetime import datetime

# =====================================================
# APP INFO
# =====================================================

APP_NAME = "JSON Generator Pro"
VERSION = "2.0"

# =====================================================
# USER / OUTPUT SETTINGS
# =====================================================

current_user = getpass.getuser()

if getattr(sys, "frozen", False):
    app_folder = os.path.dirname(sys.executable)
else:
    app_folder = os.path.dirname(os.path.abspath(__file__))

output_folder = os.path.join(app_folder, "JSON_Output")

os.makedirs(output_folder, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(output_folder, "generator.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# =====================================================
# FUNCTIONS
# =====================================================

def browse_folder():
    global output_folder

    folder = filedialog.askdirectory(
        title="Select Output Folder"
    )

    if folder:
        output_folder = folder
        folder_label.config(text=folder)
        status_label.config(
            text=f"Output Folder: {folder}"
        )


def load_file():

    filename = filedialog.askopenfilename(
        filetypes=[
            ("Text Files", "*.txt"),
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ]
    )

    if not filename:
        return

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            input_box.delete(
                "1.0",
                tk.END
            )

            input_box.insert(
                tk.END,
                file.read()
            )

        status_label.config(
            text=f"Loaded: {os.path.basename(filename)}"
        )

    except Exception as e:

        messagebox.showerror(
            "File Error",
            str(e)
        )


def clear_text():

    input_box.delete(
        "1.0",
        tk.END
    )

    preview_box.delete(
        "1.0",
        tk.END
    )

    progress["value"] = 0


def open_folder():

    if os.path.exists(output_folder):
        os.startfile(output_folder)


def copy_preview():

    text = preview_box.get(
        "1.0",
        tk.END
    )

    root.clipboard_clear()
    root.clipboard_append(text)

    status_label.config(
        text="Preview copied to clipboard"
    )


def search_preview():

    preview_box.tag_remove(
        "highlight",
        "1.0",
        tk.END
    )

    search_text = search_var.get()

    if not search_text:
        return

    start = "1.0"

    while True:

        start = preview_box.search(
            search_text,
            start,
            stopindex=tk.END
        )

        if not start:
            break

        end = f"{start}+{len(search_text)}c"

        preview_box.tag_add(
            "highlight",
            start,
            end
        )

        start = end

    preview_box.tag_config(
        "highlight",
        background="yellow",
        foreground="black"
    )


def generate_json():

    text = input_box.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        messagebox.showerror(
            "Error",
            "No data entered."
        )

        return

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    generated_files = []
    devices_seen = set()

    invalid_lines = []
    duplicate_lines = []

    preview_box.delete(
        "1.0",
        tk.END
    )

    lines = text.splitlines()

    progress["maximum"] = len(lines)
    progress["value"] = 0

    for line_num, line in enumerate(
        lines,
        start=1
    ):

        progress["value"] = line_num
        root.update_idletasks()

        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) != 2:

            invalid_lines.append(
                f"Line {line_num}: {line}"
            )

            continue

        account = parts[0]
        device = parts[1]

        if device in devices_seen:

            duplicate_lines.append(device)

            continue

        devices_seen.add(device)

        data = {
            "device": device,
            "account": account,
            "created_by": current_user,
            "created_date": timestamp,
            "account_rotation_enabled": True,
            "override_maintenance_window": None,
            "override_refresh_frequency": None
        }

        filepath = os.path.join(
            output_folder,
            f"{device}.json"
        )

        try:

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=2
                )

            generated_files.append(
                filepath
            )

            preview_box.insert(
                tk.END,
                json.dumps(
                    data,
                    indent=2
                ) + "\n\n"
            )

        except Exception as e:

            invalid_lines.append(
                f"{device}: {str(e)}"
            )

    zip_path = os.path.join(
        output_folder,
        f"devices_{timestamp}.zip"
    )

    try:

        with zipfile.ZipFile(
            zip_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for json_file in generated_files:

                zipf.write(
                    json_file,
                    os.path.basename(json_file)
                )

        logging.info(
            f"{current_user} generated "
            f"{len(generated_files)} files"
        )

    except Exception as e:

        messagebox.showerror(
            "ZIP Error",
            str(e)
        )

        return

    result_message = (
        f"Generated {len(generated_files)} JSON files\n\n"
        f"ZIP Created:\n{zip_path}"
    )

    if duplicate_lines:

        result_message += (
            "\n\nDuplicates:\n"
            + "\n".join(duplicate_lines)
        )

    if invalid_lines:

        result_message += (
            "\n\nInvalid Entries:\n"
            + "\n".join(invalid_lines)
        )

    messagebox.showinfo(
        "Complete",
        result_message
    )

    status_label.config(
        text=f"Generated {len(generated_files)} JSON files"
    )

# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()

root.title(
    f"{APP_NAME} v{VERSION}"
)

root.geometry(
    "1400x850"
)

root.configure(
    bg="#1e1e1e"
)

# =====================================================
# TITLE
# =====================================================

title = tk.Label(
    root,
    text=f"{APP_NAME} v{VERSION}",
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 18, "bold")
)

title.pack(pady=10)

# =====================================================
# SEARCH BOX
# =====================================================

search_var = tk.StringVar()

search_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

search_frame.pack()

tk.Label(
    search_frame,
    text="Search Preview:",
    bg="#1e1e1e",
    fg="white"
).pack(side="left")

tk.Entry(
    search_frame,
    textvariable=search_var,
    width=40
).pack(
    side="left",
    padx=5
)

tk.Button(
    search_frame,
    text="Search",
    command=search_preview
).pack(
    side="left"
)

# =====================================================
# BUTTON BAR
# =====================================================

button_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

button_frame.pack(
    pady=10
)

buttons = [

    ("Load File", load_file),

    ("Browse Folder", browse_folder),

    ("Generate JSON", generate_json),

    ("Copy Preview", copy_preview),

    ("Clear", clear_text),

    ("Open Folder", open_folder)
]

for col, (text, cmd) in enumerate(buttons):

    tk.Button(
        button_frame,
        text=text,
        command=cmd
    ).grid(
        row=0,
        column=col,
        padx=5
    )

# =====================================================
# OUTPUT FOLDER LABEL
# =====================================================

folder_label = tk.Label(
    root,
    text=output_folder,
    bg="#1e1e1e",
    fg="lightgreen"
)

folder_label.pack()

# =====================================================
# PROGRESS BAR
# =====================================================

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=500,
    mode="determinate"
)

progress.pack(
    pady=5
)

# =====================================================
# MAIN PANELS
# =====================================================

main_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

input_box = tk.Text(
    main_frame,
    bg="#252526",
    fg="white",
    insertbackground="white",
    font=("Consolas", 11)
)

input_box.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)

preview_box = tk.Text(
    main_frame,
    bg="#252526",
    fg="#7CFC00",
    insertbackground="white",
    font=("Consolas", 11)
)

preview_box.pack(
    side="right",
    fill="both",
    expand=True,
    padx=5
)

# =====================================================
# RIGHT CLICK MENU
# =====================================================

context_menu = tk.Menu(
    root,
    tearoff=0
)

context_menu.add_command(
    label="Cut",
    command=lambda:
    input_box.event_generate("<<Cut>>")
)

context_menu.add_command(
    label="Copy",
    command=lambda:
    input_box.event_generate("<<Copy>>")
)

context_menu.add_command(
    label="Paste",
    command=lambda:
    input_box.event_generate("<<Paste>>")
)

context_menu.add_separator()

context_menu.add_command(
    label="Select All",
    command=lambda:
    input_box.tag_add(
        "sel",
        "1.0",
        "end"
    )
)

def show_context_menu(event):

    context_menu.tk_popup(
        event.x_root,
        event.y_root
    )

input_box.bind(
    "<Button-3>",
    show_context_menu
)

# =====================================================
# STATUS BAR
# =====================================================

status_label = tk.Label(
    root,
    text="Ready",
    anchor="w",
    relief=tk.SUNKEN
)

status_label.pack(
    side=tk.BOTTOM,
    fill=tk.X
)

root.mainloop()
