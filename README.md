# 🤖 RAG Chatbot — Sistemas de Informação · IFSULDEMINAS

Chatbot RAG (Retrieval-Augmented Generation) com **Flask + ChromaDB + Google AI Studio (Gemini)** no backend e **React** no frontend.

---

## 📁 Estrutura do Projeto

```
rag-chatbot/
├── backend/
│   ├── app.py            # API Flask principal
│   ├── seed_data.py      # Script para popular o ChromaDB
│   ├── requirements.txt
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx       # Componente principal do chat
│   │   ├── App.css       # Estilos
│   │   └── index.js      # Entry point React
│   ├── package.json
│   └── .gitignore
└── README.md
```

---

## 🚀 Como rodar localmente

### Pré-requisitos
- Python 3.10+
- Node.js 18+
- Chave de API do Google AI Studio (gratuita em https://aistudio.google.com)

---

### 1. Backend (Flask + ChromaDB)

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variável de ambiente
cp .env.example .env
# Edite o .env e coloque sua GOOGLE_API_KEY

# Iniciar o servidor
python app.py
```

O backend estará disponível em **http://localhost:5000**

#### Popular o ChromaDB com dados iniciais:
```bash
# Com o servidor rodando, em outro terminal:
python seed_data.py
```

---

### 2. Frontend (React)

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variável de ambiente
cp .env.example .env
# O .env já aponta para http://localhost:5000 por padrão

# Iniciar o React
npm start
```

O frontend estará disponível em **http://localhost:3000**

---

## 📚 Tecnologias utilizadas

- **Python / Flask** — API REST do backend
- **ChromaDB** — banco de dados vetorial para embeddings
- **Google Generative AI (Gemini)** — embeddings + geração de resposta
- **React 18** — interface do chatbot
- **Axios** — requisições HTTP
- **React Markdown** — renderização de markdown nas respostas
