import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

// ─── Icons ────────────────────────────────────────────────────────────────────
const BotIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" className="icon">
    <rect x="3" y="8" width="18" height="13" rx="3" stroke="currentColor" strokeWidth="1.8" />
    <circle cx="9" cy="14" r="1.5" fill="currentColor" />
    <circle cx="15" cy="14" r="1.5" fill="currentColor" />
    <path d="M9 19h6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    <path d="M12 8V5M10 5h4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
  </svg>
);

const SendIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" className="icon-sm">
    <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    <path d="M22 2L15 22l-4-9-9-4 20-7z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const SourceIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" className="icon-xs">
    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z" stroke="currentColor" strokeWidth="1.8" />
    <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
  </svg>
);

const TrashIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" className="icon-sm">
    <path d="M3 6h18M19 6l-1 14H6L5 6M10 11v6M14 11v6M9 6V4h6v2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const DatabaseIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" className="icon-sm">
    <ellipse cx="12" cy="5" rx="9" ry="3" stroke="currentColor" strokeWidth="1.8" />
    <path d="M3 5v5c0 1.66 4.03 3 9 3s9-1.34 9-3V5" stroke="currentColor" strokeWidth="1.8" />
    <path d="M3 10v5c0 1.66 4.03 3 9 3s9-1.34 9-3v-5" stroke="currentColor" strokeWidth="1.8" />
    <path d="M3 15v4c0 1.66 4.03 3 9 3s9-1.34 9-3v-4" stroke="currentColor" strokeWidth="1.8" />
  </svg>
);

// ─── Suggestion chips ──────────────────────────────────────────────────────────
const SUGGESTIONS = [
  "O que são vulnerabilidades Zero-Day?",
  "Diferença entre SAST e DAST?",
  "O que a LGPD define como dado sensível?",
  "O que é arquitetura Zero Trust?",
  "Quais as etapas de um Plano de Resposta a Incidentes?",
];

// ─── Main Component ────────────────────────────────────────────────────────────
export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [docsCount, setDocsCount] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [ingestText, setIngestText] = useState("");
  const [ingestSource, setIngestSource] = useState("");
  const [ingestMsg, setIngestMsg] = useState("");
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    checkHealth();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function checkHealth() {
    try {
      const res = await axios.get(`${API_URL}/health`);
      setDocsCount(res.data.docs_count);
    } catch {
      setDocsCount("—");
    }
  }

  async function sendMessage(text) {
    const question = text || input.trim();
    if (!question) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const res = await axios.post(`${API_URL}/chat`, { question });
      const { answer, sources } = res.data;
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: answer, sources: sources || [] },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Erro ao conectar com o backend. Verifique se o servidor Flask está rodando.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function handleIngest() {
    if (!ingestText.trim()) return;
    setIngestMsg("Enviando...");
    try {
      const doc = {
        id: `manual_${Date.now()}`,
        text: ingestText.trim(),
        metadata: { source: ingestSource || "Inserção manual", categoria: "Manual" },
      };
      const res = await axios.post(`${API_URL}/ingest`, { documents: [doc] });
      setIngestMsg(res.data.message);
      setIngestText("");
      setIngestSource("");
      checkHealth();
    } catch {
      setIngestMsg("Erro ao inserir documento.");
    }
  }

  async function clearChat() {
    setMessages([]);
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="header">
        <div className="header-left">
          <div className="logo-wrapper">
            <BotIcon />
          </div>
          <div>
            <h1 className="header-title">Cyber Chat</h1>
            <p className="header-sub">Sistemas de Informação · IFSULDEMINAS</p>
          </div>
        </div>
        <div className="header-right">
          {docsCount !== null && (
            <span className="badge">
              <DatabaseIcon /> {docsCount} docs
            </span>
          )}
          <button className="btn-icon" onClick={() => setSidebarOpen(!sidebarOpen)} title="Gerenciar base">
            <DatabaseIcon />
          </button>
          <button className="btn-icon" onClick={clearChat} title="Limpar conversa">
            <TrashIcon />
          </button>
        </div>
      </header>

      <div className="main">
        {/* ── Chat ── */}
        <div className="chat-area">
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon"><BotIcon /></div>
              <h2>Olá! Sou o Cyber Assistant 👋</h2>
              <p>Sou seu consultor especializado em <strong>Cibersegurança</strong>, <strong>Governança de Dados</strong> e <strong>LGPD</strong>. Experimente perguntar:</p>
              <div className="suggestions">
                {SUGGESTIONS.map((s) => (
                  <button key={s} className="chip" onClick={() => sendMessage(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((msg, i) => (
                <div key={i} className={`message-row ${msg.role}`}>
                  {msg.role === "assistant" && (
                    <div className="avatar bot-avatar"><BotIcon /></div>
                  )}
                  <div className={`bubble ${msg.role}`}>
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                    {msg.role === "assistant" && msg.sources?.length > 0 && (
                      <div className="sources">
                        <SourceIcon />
                        <span>Fontes: {msg.sources.filter(Boolean).join(" · ")}</span>
                      </div>
                    )}
                  </div>
                  {msg.role === "user" && (
                    <div className="avatar user-avatar">U</div>
                  )}
                </div>
              ))}
              {loading && (
                <div className="message-row assistant">
                  <div className="avatar bot-avatar"><BotIcon /></div>
                  <div className="bubble assistant loading-bubble">
                    <span className="dot" /><span className="dot" /><span className="dot" />
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        {/* ── Input ── */}
        <div className="input-area">
          <div className="input-wrapper">
            <textarea
              ref={inputRef}
              className="chat-input"
              placeholder="Faça uma pergunta sobre a base de conhecimento..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              rows={1}
              disabled={loading}
            />
            <button
              className="send-btn"
              onClick={() => sendMessage()}
              disabled={loading || !input.trim()}
            >
              <SendIcon />
            </button>
          </div>
          <p className="input-hint">Enter para enviar · Shift+Enter para nova linha</p>
        </div>
      </div>

      {/* ── Sidebar Gerenciar Base ── */}
      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)}>
          <div className="sidebar" onClick={(e) => e.stopPropagation()}>
            <div className="sidebar-header">
              <h3>Gerenciar Base</h3>
              <button className="btn-close" onClick={() => setSidebarOpen(false)}>✕</button>
            </div>
            <div className="sidebar-body">
              <p className="sidebar-info">
                <DatabaseIcon /> <strong>{docsCount}</strong> documentos indexados
              </p>
              <hr className="divider" />
              <h4>Inserir novo documento</h4>
              <input
                className="sidebar-input"
                placeholder="Fonte / título (ex: Relatório de Ameaças)"
                value={ingestSource}
                onChange={(e) => setIngestSource(e.target.value)}
              />
              <textarea
                className="sidebar-textarea"
                placeholder="Cole aqui o texto do documento..."
                value={ingestText}
                onChange={(e) => setIngestText(e.target.value)}
                rows={6}
              />
              <button className="btn-primary" onClick={handleIngest}>
                Inserir na Base
              </button>
              {ingestMsg && <p className="ingest-msg">{ingestMsg}</p>}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}