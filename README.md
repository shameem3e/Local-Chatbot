# 📚 Local Chatbot  

A **private ChatGPT-like application** that integrates multiple model providers — **Ollama (local)**, **Groq (cloud API)**, and **OpenAI (cloud API)** — into one unified chatbot interface. This allows you to experiment with both **local lightweight models** and **state-of-the-art hosted models** seamlessly.  

---

## 📌 Features
- 🖥️ **Run local models** (Mistral, Gemma via Ollama) without internet.  
- ☁️ **Access hosted models** (Groq & OpenAI) with blazing speed.  
- 🔑 **Switch providers easily** using `models_config.yaml`.  
- ⚡ Lightweight backend + frontend for chat interactions.  
- 🔒 Private setup — no external tracking.  

---

## 📂 Folder Structure
Local-Chatbot/

├── backend/ # Backend code (FastAPI or similar)

│ ├── api/ # API endpoints and related services

│ │ ├── chat.py # Main chat API logic

│ │ ├── conversation.py # Handles conversation/session logic

│ │ ├── db_services.py # Database service functions

│ │ ├── provider_models.py # Model provider integration logic

│ │ └── title.py # Utility for chat titles

│ │

│ ├── config/ # Backend configuration

│ │ ├── init.py

│ │ ├── backend_config.py # Backend settings

│ │ └── models_config.yaml # Defines available models & providers

│ │

│ ├── db/ # Database access objects

│ │ ├── init.py

│ │ └── chat_da o.py # Chat database access operations

│ │

│ ├── llm/ # LLM factory/abstractions

│ │ ├── init.py

│ │ └── llm_factory.py # Factory pattern to select models

│ │

│ ├── services/ # Backend service layer

│ │ ├── chat.py

│ │ ├── db_services.py

│ │ ├── provider_models.py

│ │ └── title.py

│ │

│ └── main.py # Backend entry point

│

├── data/ # Data directory

│ └── placeholder.txt

│

├── frontend/ # Frontend app (Streamlit)

│ ├── config/

│ │ ├── init.py

│ │ └── frontend_config.py # Frontend configuration

│ ├── init.py

│ └── app.py # Streamlit app entry point

│

├── .env # Environment variables (API keys, configs)

└── requirements.txt # Python dependencies

---

## ​​ Setup Guide

### **1️⃣ Install Prerequisites**
Before you begin, make sure you have:

- **Python 3.8+** installed on your system
- (If using local models) **Ollama** installed and configured
- API keys for any hosted models (if applicable)

#### Local Models (Ollama)
- Install via [Ollama Download](https://ollama.com/download/) for Windows.
- Run in PowerShell:
```powershell
ollama run mistral        # installs and runs Mistral:7B by default
ollama run gemma:2b       # installs and runs Gemma 2B
```
#### Hosted Models (API-based)

If you integrate hosted LLMs (e.g., Groq or OpenAI):

* Groq: Register at [Groq Cloud Console](https://console.groq.com/home), get your API key, then:
- Run in Terminal:
```terminal
pip install groq
setx GROQ_API_KEY "your_api_key_here"
```
* OpenAI: Sign up on [OpenAI platform](https://platform.openai.com), get API key, then:
- Run in Terminal:
```terminal
pip install openai
setx OPENAI_API_KEY "your_api_key_here"
```
### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/shameem3e/Local-Chatbot.git
cd Local-Chatbot
```

### **3️⃣ Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
### **4️⃣ Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **5️⃣ Run the project**
Launch both backend and frontend:
* Backend (e.g., FastAPI):
- Run in Terminal:
```terminal
uvicorn backend.main:app --reload
```
This will show to open `localhost:8501` 

* Frontend (Streamlit UI):
- Run in new Terminal(Don't close Backend terminal):
```terminal
streamlit run frontend/app.py
```
This will shows to open `localhost:8000`, Which allows you to open Chatbot in your browser.

### **💻 Command Reference**
```bash
Open New Chat
Select your model upon clicking settings icon
Enter your Text
```
### **✅ Example Output**
You:
```bash
Hello, what can you do?
```
Local Chatbot:
```bash
Hi! I can chat using local LLMs (via Ollama) or call Groq/OpenAI models based on your config.
```

---

## 📜 Code Overview

### **Backend** 
 `backend/main.py` 
* **Purpose**: Entry point for running the backend (FastAPI server). 
* **Libraries**: 
	* `fastapi` → to define the API server. 
	* `uvicorn` → ASGI server to run FastAPI. 
* **Why**: Exposes backend services for chatbot through API.

---

#### **API Layer**(`backend/api/`) 
 `backend/api/chat.py` 
* **Purpose**: Handles chat requests and responses via API endpoints.
* **Libraries**: 
	* `fastapi.APIRouter` → for route definition. 
	* `pydantic` → request/response validation.
* **Why**: Main communication bridge between frontend and chatbot backend.

 `backend/api/conversation.py` 
* **Purpose**: Manages conversation state and sessions.
* **Libraries**: 
	* Python’s `uuid` or session libraries → for unique conversation IDs.
	* **Why**: Keeps track of ongoing multi-turn dialogues.

 `backend/api/db_services.py` 
* **Purpose**: API wrapper to fetch and store chat data in database.
* **Libraries**: 
	* `sqlalchemy` or `sqlite3` → database operations.
* **Why**: Decouples DB logic from core APIs.

 `backend/api/provider_models.py` 
* **Purpose**: Defines which external LLM provider (Ollama, Groq, OpenAI) to call.
* **Libraries**: 
	* `httpx` / `requests` → HTTP calls to providers.
* **Why**: Makes chatbot extensible across multiple model providers.

 `backend/api/title.py` 
* **Purpose**: Generates titles for chat sessions automatically.
* **Libraries**: 
	* LLM API calls (OpenAI, etc.)
* **Why**: Improves user experience by organizing conversations.

---

#### **Config Layer**(`backend/config/`) 
 `backend/config/backend_config.py` 
* **Purpose**: Stores backend-specific configuration (server host, ports).
* **Libraries**: 
	* `pydantic.BaseSettings` / `os` → environment configs.
* **Why**: Keeps environment-dependent variables in one place.

 `backend/config/models_config.yaml` 
* **Purpose**: YAML file defining which LLM models/providers are available.
* **Libraries**: 
	* `pyyaml` → parse YAML.
* **Why**: Easy to add/remove LLM models without changing code.

---

#### **Database Layer**(`backend/db/`) 
 `backend/db/chat_dao.py` 
* **Purpose**: DAO (Data Access Object) for chat records. Encapsulates database queries.
* **Libraries**: 
	* `sqlalchemy` or `sqlite3` 
* **Why**: Ensures clean DB operations and separation from business logic.

---

#### **LLM Layer**(`backend/llm/`) 
 `backend/llm/llm_factory.py` 
* **Purpose**: Factory pattern to dynamically load the correct model provider (Ollama, Groq, OpenAI).
* **Libraries**: 
	* Python OOP (classes, factory pattern). 
* **Why**: Makes chatbot provider-agnostic and modular.

---

#### **Service Layer**(`backend/service/`)
These mirror `api/` files but handle business logic (decoupled from API definitions).
 `backend/services/chat.py`
* **Purpose**: Core chat logic (generate response, clean input, call LLM).
* **Libraries**:
 	* LLM SDKs (Ollama, OpenAI, etc.).
* **Why**: Keeps backend logic separate from API endpoints.

`backend/services/db_services.py` 
* **Purpose**: Business layer for DB operations (save/retrieve chats).
* **Libraries**: 
	* `sqlalchemy` / `sqlite3` 
* **Why**: Avoids mixing raw DB code with API.

`backend/services/provider_models.py` 
* **Purpose**: Handles model API calls in service layer.
* **Libraries**: 
	* `requests` / `httpx` 
* **Why**: Abstracts away provider communication.

`backend/services/title.py` 
* **Purpose**: Business logic for title generation.
* **Libraries**: 
	* LLM API calls.
* **Why**: Title generation handled separately from API.

---

### **Frontend** 
 `frontend/app.py` 
* **Purpose**: Entry point for Streamlit frontend app. 
* **Libraries**: 
	* `streamlit` → UI framework. 
	* `requests` → calls backend API. 
* **Why**: Provides simple web interface for chatting.

---

#### **Frontend Config**(`frontend/config/`) 
 `frontend/config/frontend_config.py` 
* **Purpose**: Stores frontend-related configs (API endpoint URLs, theme).
* **Libraries**: 
	* `os`,`dotenv`
* **Why**: Keeps frontend settings centralized.

---

### **Data Folder** 
 `data/placeholder.txt` 
* **Purpose**: Keeps the data/ folder in Git (since empty folders aren’t committed). 

---

### **Root Files** 
 `.env` 
* **Purpose**: Stores sensitive keys (OpenAI API, Groq API, DB connection strings). 
* **Libraries**: 
	* `python-dotenv`
* **Why**: Keeps secrets out of source code.

---

## ❓ FAQ

**Q1: Do I need the internet to use this chatbot?**  
- No (for Ollama) → You can run local LLMs like Mistral or Gemma entirely offline.
- Yes (for Groq / OpenAI) → These providers require an active internet connection and API keys. 

**Q2: Can I use multiple models in one session?**  
- Yes! You can switch between providers (`Ollama`, `Groq`, `OpenAI`) seamlessly through `models_config.yaml` or frontend settings.

**Q3. Where are my conversations stored?**
- Chats are stored locally in the SQLite database (`backend/db/chat_dao.py`).
- Nothing is shared externally unless you explicitly use Groq/OpenAI APIs.

**Q4. How do I add a new model provider?**
- Update `models_config.yaml` with the new provider details.
- Extend `llm_factory.py` to load the provider.
- Add any required API key to `.env`.

**Q5. Can I run this on Windows/Mac/Linux?**
- Yes, it’s fully cross-platform.
- For Windows users, ensure Ollama and Python are installed properly.

**Q6. Does this support GPU acceleration?**
- Ollama uses your local GPU automatically if available.
- Groq/OpenAI run on their own GPU-powered servers.

**Q7. Is my data private?**
- Yes. All local chats stay on your system.
- Only requests sent to Groq/OpenAI APIs leave your machine.  


**Q3: Can I mark tasks as done or delete them?**  
- Yes, using `done <id>` or `delete <id>` commands.  

**Q4: How do recurring tasks work?**  
- You can specify recurrence like `"daily 07:00"`, `"every monday 09:30"`, or `"monthly day 1 10:00"`.  

**Q5: How can I export tasks to a calendar?**  
- Use the `export` command to generate `.ics` files.  

**Q6: Can I run it on Windows/macOS/Linux?**  
- Yes, it’s cross-platform. Make sure you have Python 3.10+ and the required toolchain for `llama-cpp-python`.

---

## 🛠 Tech Stack

### Backend
- **FastAPI** – Async API framework for performance.  
- **Uvicorn** – Runs the FastAPI backend.  
- **SQLAlchemy** / **sqlite3** – Lightweight DB storage. 
- **PyYAML** – Parse `models_config.yaml` for providers.  
- **httpx** – `Async HTTP client for API calls.
- **python-dotenv** – Manage environment variables.  

---
### LLM Providers
- **Ollama** – Local models like Mistral, Gemma.  
- **Groq API** – High-speed cloud inference.  
- **OpenAI API** – Access GPT family of models.

---
### Frontend
- **Streamlit** – Simple, interactive UI.  
- **Requests** – Connect frontend to backend. 

---
### General
- **Python 3.8+** – Base language.  
- **dotenv / os** – Config handling.  
- **logging** – Debugging & monitoring.

---

## 🚀 Future Improvements

- 🔎 **RAG Integration** → Enhance answers with local document knowledge.
- 👥 **Multi-user Support** → Separate sessions for multiple users.
- 💾 **Export/Import Chats** → Save or restore chat history easily.
- 🎨 **Enhanced UI** → More customization in frontend (themes, markdown, rich media).
- 📊 **Analytics Dashboard** → Track usage, model performance, and latency.
- 🧠 **Custom Fine-tuned Models** → Support user-uploaded fine-tuned LLMs.
- 📡 **WebSocket Support** → Real-time streaming responses (like ChatGPT).

---

## 👨‍💻 Author
[MD. Shameem Ahammed](https://sites.google.com/view/shameem3e)

Graduate Student | AI & ML Enthusiast

---
