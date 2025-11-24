import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import tkinter as tk
from tkinter import scrolledtext
import customtkinter as ctk
import threading
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

# Theme colors
DARK_THEME = {
    "bg": "#0a0e27",
    "fg": "#00d9ff",
    "text_bg": "#151b3d",
    "text_fg": "#ffffff",
    "button_bg": "#1e2749",
    "button_fg": "#00d9ff",
    "status_bg": "#1e2749",
    # bubble colors
    "jarvis_bubble_bg": "#003366",
    "jarvis_bubble_text": "#C3F8FF",
    "user_bubble_bg": "#1e2749",
    "user_bubble_text": "#E8D3FF"
}

LIGHT_THEME = {
    "bg": "#f0f0f0",
    "fg": "#0066cc",
    "text_bg": "#ffffff",
    "text_fg": "#000000",
    "button_bg": "#e0e0e0",
    "button_fg": "#0066cc",
    "status_bg": "#e0e0e0",
    # bubble colors
    "jarvis_bubble_bg": "#C3F8FF",
    "jarvis_bubble_text": "#003366",
    "user_bubble_bg": "#E8D3FF",
    "user_bubble_text": "#000000"
}

current_theme = DARK_THEME
is_listening = False
should_stop = False

def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def update_conversation(text, speaker="Jarvis"):
    bubble_frame = ctk.CTkFrame(scrollable_frame, fg_color=current_theme["bg"], corner_radius=0)
    
    wrap = root.winfo_width() - 80
    font_size = 14

    # Bubble styling
    if speaker == "Jarvis":
        bubble = ctk.CTkLabel(
            bubble_frame,
            text=text,
            fg_color=current_theme["jarvis_bubble_bg"],       # bubble color
            text_color=current_theme["jarvis_bubble_text"],
            wraplength=wrap,  # responsive
            corner_radius=15,          # rounded corners
            justify="left",
            padx=15, pady=10,
            font=("Poppins", font_size)
        )
        bubble.pack(anchor="w", pady=8, padx=10)
    else:
        bubble = ctk.CTkLabel(
            bubble_frame,
            text=text,
            fg_color=current_theme["user_bubble_bg"],
            text_color=current_theme["user_bubble_text"],
            wraplength=wrap,
            corner_radius=15,
            justify="right",
            padx=15, pady=10,
            font=("Poppins", font_size)
        )
        bubble.pack(anchor="e", pady=8, padx=10)

    bubble_frame.pack(fill='x', pady=6, padx=10)

    # Scroll to bottom smoothly
    root.update_idletasks()
    canvas.yview_moveto(1.0)

def update_status(text, color=None):
    if color is None:
        color = current_theme["fg"]
    status_label.configure(text="● Listening...", text_color="#00ff00")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_status("Listening...", "#00ff00")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        update_status("Processing...", "#ffaa00")
        try:
            query = r.recognize_google(audio, language="en-in")
            update_conversation(query, "User")
            return query
        except sr.UnknownValueError:
            update_status("Ready", current_theme["fg"])
            say("Sorry, I did not understand that.")
            update_conversation("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            update_status("Error", "#ff0000")
            say("Could not request results; check your internet connection.")
            update_conversation("Could not request results; check your internet connection.")
            return None

def process_command(query):
    if not query:
        return
    
    update_status("Speaking...", "#00d9ff")
    
    # YouTube search
    if "youtube" in query.lower() and ("search" in query.lower() or "find" in query.lower() or "play" in query.lower()):
        search_term = query.lower().replace("search", "").replace("find", "").replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
        response = f"Searching {search_term} on YouTube"
        say(response)
        update_conversation(response)
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
    
    # Google search
    elif "google" in query.lower() and ("search" in query.lower() or "find" in query.lower()):
        search_term = query.lower().replace("search", "").replace("find", "").replace("on google", "").replace("google", "").strip()
        response = f"Searching {search_term} on Google"
        say(response)
        update_conversation(response)
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
    
    # Open websites
    elif "open" in query.lower():
        sites = [["youtube", "https://youtube.com"], 
                 ["wikipedia", "https://wikipedia.com"], 
                 ["google", "https://google.com"], 
                 ["gmail", "https://gmail.com"], 
                 ["spotify", "https://spotify.com"], 
                 ["netflix", "https://netflix.com"],
                 ["chatgpt", "https://chatgpt.com"]]
        for site in sites:
            if site[0] in query.lower():
                response = f"Opening {site[0]}"
                say(response)
                update_conversation(response)
                webbrowser.open(site[1])
                break
    
    # Tell time
    elif "time" in query.lower():
        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The time is {strfTime}"
        say(response)
        update_conversation(response)
    
    # Theme toggle
    elif "dark theme" in query.lower() or "dark mode" in query.lower():
        toggle_theme(force="dark")
        response = "Switched to dark theme"
        say(response)
        update_conversation(response)
    
    elif "light theme" in query.lower() or "light mode" in query.lower():
        toggle_theme(force="light")
        response = "Switched to light theme"
        say(response)
        update_conversation(response)
    
    # Exit
    elif "exit" in query.lower() or "stop" in query.lower() or "quit" in query.lower():
        global should_stop
        should_stop = True
        response = "Goodbye!"
        say(response)
        update_conversation(response)
        update_status("Offline", "#ff0000")
        root.quit()
    
    else:
         response = ask_gpt(query)
         say(response)
         update_conversation(response)

    update_status("Ready", current_theme["fg"])

def start_listening():
    global is_listening, should_stop
    if not is_listening:
        is_listening = True
        should_stop = False
       # mic_button.config(text="🎤 Listening (Click to Stop)", command=stop_listening)  # ← Changed text and added stop function
        
        def listen_loop():  # ← Renamed from listen_thread
            global is_listening, should_stop
            while not should_stop:  # ← WHILE LOOP! Keeps listening forever
                query = takeCommand()
                if query:
                    process_command(query)
                    if should_stop:
                        break
            is_listening = False
          #  mic_button.config(text="🎤 Start Listening", state='normal', command=start_listening)
        
        thread = threading.Thread(target=listen_loop)
        thread.daemon = True
        thread.start()

def stop_listening():  # ← NEW FUNCTION ADDED
    global should_stop
    should_stop = True
    update_status("Stopping...", "#ff0000")
   # mic_button.config(state='disabled')

def ask_gpt(prompt):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

    
def toggle_theme(force=None):
    global current_theme
    
    if force == "dark":
        current_theme = DARK_THEME
        ctk.set_appearance_mode("dark")
    elif force == "light":
        current_theme = LIGHT_THEME
        ctk.set_appearance_mode("light")
    else:
        current_theme = LIGHT_THEME if current_theme == DARK_THEME else DARK_THEME
        ctk.set_appearance_mode("light" if current_theme==LIGHT_THEME else "dark")
    
    # --- Update root and main frames ---
    root.config(bg=current_theme["bg"])
    header_frame.config(bg=current_theme["bg"])
    title_label.config(bg=current_theme["bg"], fg=current_theme["fg"])
    theme_button.configure(fg_color=current_theme["button_bg"], text_color=current_theme["button_fg"])
    
    conversation_frame.config(bg=current_theme["bg"])
    canvas.config(bg=current_theme["bg"])
    scrollable_frame.config(bg=current_theme["bg"])
    
    control_frame.config(bg=current_theme["bg"])
    
    status_frame.configure(fg_color=current_theme["status_bg"])
    status_label.configure(fg_color=current_theme["status_bg"], text_color=current_theme["fg"])
    
    scrollbar.config(troughcolor=current_theme["bg"], bg=current_theme["bg"], highlightbackground=current_theme["bg"])
    
    # --- Update all chat bubbles ---
    for bubble_frame in scrollable_frame.winfo_children():
        bubble_frame.configure(fg_color=current_theme["bg"])  # <-- update parent frame bg
        for bubble in bubble_frame.winfo_children():
            if isinstance(bubble, ctk.CTkLabel):
               if bubble.cget("justify") == "left":  # Jarvis
                  bubble.configure(
                    fg_color=current_theme["jarvis_bubble_bg"],
                    text_color=current_theme["jarvis_bubble_text"]
                )
               else:  # User
                  bubble.configure(
                    fg_color=current_theme["user_bubble_bg"],
                    text_color=current_theme["user_bubble_text"]
                )


# Create GUI
root = tk.Tk()
def on_resize(event):
    canvas.configure(width=event.width - 40)

root.bind("<Configure>", on_resize)

root.title("Jarvis AI Assistant")
root.geometry("600x700")
root.config(bg=DARK_THEME["bg"])

# Header
header_frame = tk.Frame(root, bg=DARK_THEME["bg"])
header_frame.pack(fill='x', padx=20, pady=20)

title_label = tk.Label(header_frame, text="J.A.R.V.I.S", font=("Arial", 28, "bold"), 
                        bg=DARK_THEME["bg"], fg=DARK_THEME["fg"])
title_label.pack(side='left')

theme_button = ctk.CTkButton(
    header_frame, text="☀️/🌙", font=("Arial",18,"bold"),
    fg_color=DARK_THEME["button_bg"], text_color=DARK_THEME["button_fg"],
    corner_radius=10, command=lambda: toggle_theme()
)
theme_button.pack(side="right")

# Conversation Area (Bubble Chat Layout)
conversation_frame = tk.Frame(root, bg=current_theme["bg"])
conversation_frame.pack(fill='both', expand=True, padx=20, pady=10)

canvas = tk.Canvas(conversation_frame, bg=current_theme["bg"], highlightthickness=0)
scrollbar = tk.Scrollbar(conversation_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=current_theme["bg"])
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Control Frame
control_frame = tk.Frame(root, bg=DARK_THEME["bg"])
control_frame.pack(fill='x', padx=20, pady=10)

'''mic_button = ctk.CTkButton(
    control_frame, 
    text="🎤 Start Listening",
    font=("Arial", 14, "bold"),
    fg_color=DARK_THEME["button_bg"],
    text_color=DARK_THEME["button_fg"],
    command=start_listening,
    corner_radius=10,
    height=50
)
mic_button.pack(fill='x')'''


# Status Bar
status_frame = ctk.CTkFrame(root, fg_color=DARK_THEME["status_bg"], corner_radius=0)
status_frame.pack(fill='x', side='bottom')

status_label = ctk.CTkLabel(status_frame, text="● Ready", font=("Arial",10,"bold"),
                             fg_color=DARK_THEME["status_bg"], text_color=DARK_THEME["fg"],
                             anchor='w', padx=20, pady=5)
status_label.pack(fill='x')

# Initialize
update_conversation("Hello! I am Jarvis AI. Listening for your commands...")
say("Hello I am Jarvis AI")
scrollbar.config(troughcolor=current_theme["bg"], activebackground=current_theme["fg"])

# Start listening automatically
start_listening()

root.mainloop()

                         
                            
