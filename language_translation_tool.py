import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import pyperclip
import tempfile
import threading
import os
from tkinter import PhotoImage

raw_langs = GoogleTranslator().get_supported_languages(as_dict=True)

languages = {k.lower(): v for k, v in raw_langs.items()}
language_names = sorted([k.title() for k in languages.keys()])

def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter text.")
        return

    try:
        source_lang = languages[source_combo.get().lower()]
        target_lang = languages[target_combo.get().lower()]

        translated = GoogleTranslator(
            source=source_lang,
            target=target_lang
        ).translate(text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

    except Exception as e:
        messagebox.showerror(
        "Translation Error",
        f"This language pair is currently not supported.\n\n{e}"
    )

def copy_text():
    text = output_text.get("1.0", tk.END).strip()

    if text:
        pyperclip.copy(text)
        messagebox.showinfo(
            "Copied",
            "Text copied successfully!"
        )

def speak_text():

    def run():
        text = output_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning(
                "Warning",
                "Nothing to speak."
            )
            return

        try:
            lang = languages[target_combo.get().lower()]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            ) as fp:
                filename = fp.name

            tts = gTTS(
                text=text,
                lang=lang,
                slow=False
            )

            tts.save(filename)

            playsound(filename)

            os.remove(filename)

        except Exception as e:
            messagebox.showerror(
            "Speech Error",
            "Speech is not available for the selected language."
    )

    threading.Thread(target=run).start()

def swap_languages():
    src = source_combo.get()
    tgt = target_combo.get()

    source_combo.set(tgt)
    target_combo.set(src)

def toggle_dark_mode():
    global dark_mode

    if dark_mode:
        root.configure(bg="#f0f0f0")

        title.config(
            bg="#2c3e50",
            fg="white"
        )

        input_text.config(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        output_text.config(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        dark_btn.config(text="🌙 Dark Mode")

        dark_mode = False

    else:
        root.configure(bg="#1e1e1e")

        title.config(
            bg="#121212",
            fg="white"
        )

        input_text.config(
            bg="#2b2b2b",
            fg="white",
            insertbackground="white"
        )

        output_text.config(
            bg="#2b2b2b",
            fg="white",
            insertbackground="white"
        )

        dark_btn.config(text="☀️ Light Mode")

        dark_mode = True

root = tk.Tk()
dark_mode = False
root.title("AI Language Translator")

try:
    icon = PhotoImage(
        file=r"E:\Internships\CodeAlpha\AI_Language_Translator\logo.png"
    )
    root.iconphoto(True, icon)

except Exception as e:
    print("PNG icon not loaded:", e)

root.geometry("850x650")
root.minsize(850, 650)
root.resizable(True, True)
root.state("zoomed")

title = tk.Label(
    root,
    text="🌍 AI Language Translator",
    font=("Helvetica", 24, "bold"),
    fg="white",
    bg="#2c3e50",
    pady=10
)

title.pack(fill="x")

frame1 = tk.Frame(root)
frame1.pack(pady=15)

tk.Label(
    frame1,
    text="Source Language:",
    font=("Arial", 12, "bold")
).grid(row=0, column=0, padx=15)

source_combo = ttk.Combobox(
    frame1,
    values=language_names,
    width=40,
    state="readonly"
)

source_combo.grid(row=0, column=1, padx=10)
source_combo.set("English")

tk.Label(
    frame1,
    text="Target Language:",
    font=("Arial", 12, "bold")
).grid(row=0, column=2, padx=15)

target_combo = ttk.Combobox(
    frame1,
    values=language_names,
    width=40,
    state="readonly"
)

target_combo.grid(row=0, column=3, padx=10)
target_combo.set("Urdu")

tk.Button(
    root,
    text="🔄 Swap Languages",
    command=swap_languages,
    bg="orange",
    font=("Arial", 11, "bold")
).pack(pady=10)

dark_btn = tk.Button(
    root,
    text="🌙 Dark Mode",
    command=toggle_dark_mode,
    bg="#444444",
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
)

dark_btn.pack(pady=5)

tk.Label(
    root,
    text="Enter Text:",
    font=("Arial", 12, "bold")
).pack()

input_text = tk.Text(
    root,
    height=10,
    font=("Arial", 12)
)

input_text.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

tk.Button(
    root,
    text="Translate",
    command=translate_text,
    bg="lightgreen",
    font=("Arial", 12, "bold"),
    width=15
).pack(pady=10)

tk.Label(
    root,
    text="Translated Text:",
    font=("Arial", 12, "bold")
).pack()

output_text = tk.Text(
    root,
    height=10,
    font=("Arial", 12)
)

output_text.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

frame2 = tk.Frame(root)
frame2.pack(pady=15)

tk.Button(
    frame2,
    text="📋 Copy",
    command=copy_text,
    bg="lightblue",
    width=15
).grid(row=0, column=0, padx=10)

tk.Button(
    frame2,
    text="🔊 Speak",
    command=speak_text,
    bg="lightyellow",
    width=15
).grid(row=0, column=1, padx=10)

root.mainloop()