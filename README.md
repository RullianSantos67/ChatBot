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

## 🔑 Obter a chave do Google AI Studio

1. Acesse https://aistudio.google.com
2. Clique em **"Get API key"** no menu lateral
3. Crie um projeto e copie a chave gerada
4. Cole no arquivo `backend/.env`:
   ```
   GOOGLE_API_KEY=sua_chave_aqui
   ```

---

## 📡 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Verifica status e quantidade de docs |
| POST | `/chat` | Envia pergunta e recebe resposta RAG |
| POST | `/ingest` | Insere novos documentos no ChromaDB |
| DELETE | `/collection/clear` | Limpa todos os documentos |

### Exemplo de uso do `/chat`:
```json
POST /chat
{
  "question": "O que é RAG?"
}
```

### Exemplo de uso do `/ingest`:
```json
POST /ingest
{
  "documents": [
    {
      "id": "doc_001",
      "text": "Texto do documento aqui...",
      "metadata": { "source": "Nome da fonte", "categoria": "IA" }
    }
  ]
}
```

---

## ☁️ Deploy

### Backend no Render
1. Crie uma conta em https://render.com
2. New → Web Service → conecte seu repositório GitHub
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Adicione a variável de ambiente:** `GOOGLE_API_KEY`
4. Adicione `gunicorn` ao `requirements.txt`

### Frontend no Vercel
1. Crie uma conta em https://vercel.com
2. Import → conecte seu repositório GitHub → selecione a pasta `frontend`
3. Adicione a variável de ambiente:
   - `REACT_APP_API_URL` = URL do seu backend no Render (ex: `https://seu-app.onrender.com`)
4. Deploy!

---

## 🛠️ Personalização do Dataset

Edite o arquivo `backend/seed_data.py` e substitua os documentos pelos seus dados reais (mínimo 30 registros). Cada documento deve ter:
- `id`: identificador único
- `text`: conteúdo do documento
- `metadata.source`: nome da fonte
- `metadata.categoria`: categoria temática

---

## 📚 Tecnologias utilizadas

- **Python / Flask** — API REST do backend
- **ChromaDB** — banco de dados vetorial para embeddings
- **Google Generative AI (Gemini)** — embeddings + geração de resposta
- **React 18** — interface do chatbot
- **Axios** — requisições HTTP
- **React Markdown** — renderização de markdown nas respostas
