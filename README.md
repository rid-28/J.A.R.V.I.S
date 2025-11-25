# 🤖 JARVIS AI – Desktop Voice Assistant

A sleek, responsive, and fully functional **AI-powered desktop voice assistant** that listens continuously, responds naturally, and performs real actions like searching the web, opening websites, switching themes, and answering questions using GPT.

## 💡 Problem Solved

Most beginner Python voice assistants are basic — no GUI, no chat bubbles, no continuous listening, and very limited functionality.

This project fixes all of that.

Jarvis provides:
- A **beautiful chat-bubble interface**  
- Smooth **voice recognition + voice replies**  
- **AI-generated responses** via GPT  
- **Hands-free continuous listening**  
- Real utilities (search, open sites, tell time, switch theme)

It makes the assistant feel more human, more interactive, and actually useful.

## ✨ Features

- 🎤 **Live Speech Recognition** - Understands your voice commands in real-time.
- 🧠 **AI Responses (GPT)** - Uses OpenAI (via OpenRouter) to answer anything naturally.
- 🗣️ **Text-to-Speech Replies** - Jarvis speaks all responses clearly using `pyttsx3`.
- 💬 **Modern Chat UI**
  - Messenger-style bubbles  
  - Different colors for user & Jarvis  
  - Smooth auto-scrolling  
- 🎨 **Light & Dark Themes** - Switch instantly between modes with fully adaptive bubble colors.
- 🔍 **Smart Commands**
  - Search YouTube  
  - Search Google  
  - Open websites (YouTube, Gmail, Netflix, Spotify, Wikipedia, ChatGPT, etc.)  
  - Tell the current time  
  - Exit automatically  
- ⚙️ **Background Listening**
  - Runs on a separate thread  
  - GUI never freezes  
  - Keeps listening until stopped  
- 🖥️ **Clean CustomTkinter UI** - Rounded buttons, organized layout, responsive bubble width.

## 🛠️ Tech Stack

- **Python**
- **CustomTkinter**  
- **Tkinter**
- **SpeechRecognition**  
- **Pyttsx3**
- **OpenAI / OpenRouter API**  
- **Threading**  
- **Webbrowser & Datetime**

## 📁 Project Structure
Jarvis/
├── .vscode/
├── main.py
├── requirements.txt
├── tempCodeRunnerFile.py
└── README.md

## 🚀 Getting Started

### 1️⃣ Install Requirements

pip install -r requirements.txt

### 2️⃣ Add Your API Key  
Create a `.env` file (same folder as `main.py`) and add:

OPENROUTER_API_KEY=your_api_key_here

### 3️⃣ Run the Assistant  

python main.py

Jarvis will boot up, greet you, and start listening automatically.


## 🎨 Screenshots  


