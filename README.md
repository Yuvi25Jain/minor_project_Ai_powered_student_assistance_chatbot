📚 Student FAQ Chatbot — AI-Powered Campus Assistant
Welcome to the Student FAQ Chatbot, a modular AI assistant built to answer student queries about admissions, fees, hostels, placements, and more — powered by a vector database and ready for LLM refinement and user history logging.

This project is designed for:

🧠 Fast, context-aware responses using ChromaDB

💬 Smooth chat experience via Streamlit

🔌 Easy integration with LLMs (e.g. Mistral 7B) and SQL-based userDB

🧑‍🤝‍🧑 Team handoff with clean extension points

🛠️ Features
✅ Vector DB search using semantic similarity (ChromaDB)

✅ Streamlit UI with follow-up awareness and clean UX

✅ Flask backend with modular query handling

✅ Ready hooks for LLM post-processing and userDB logging

✅ Minimal setup — no login, no cloud dependencies

🧩 Architecture Overview
plaintext
[Streamlit UI] → [Flask Backend] → [ChromaDB Vector Search]
                             ↘
                      [Optional: LLM Refinement]
                             ↘
                      [Optional: SQL UserDB Logging]
📁 Folder Structure
plaintext
Student-Assistant-FAQ-Bot/
├── app.py                 # Flask backend
├── db.py                  # FAQ embedding into ChromaDB
├── faqs.json              # Source FAQs
├── chroma_store/          # Vector DB storage
├── ui/
│   └── streamlit_ui/
│       └── chatbot_ui.py  # Streamlit frontend
🚀 Quick Start
1. Clone the repo
bash
git clone https://github.com/Yuvi25Jain/minor_project_Ai_powered_student_assistance_chatbot.git
cd Student-Assistant-FAQ-Bot
2. Create and activate virtual environment
bash
python -m venv venv310
venv310\Scripts\activate  # Windows
3. Install dependencies
bash
pip install -r requirements.txt
4. Start ChromaDB server
bash
chroma run --path ./chroma_store
5. Embed FAQs into ChromaDB
bash
python db.py
6. Start Flask backend
bash
python app.py
7. Launch Streamlit UI
bash
cd ui/streamlit_ui
streamlit run chatbot_ui.py
🧪 Test Queries
Try asking:

“Where is the library?”

“What is the annual fee for B.Tech IT?”

“Are there scholarships for general category students?”
