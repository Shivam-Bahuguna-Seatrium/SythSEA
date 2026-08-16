import { Send } from "lucide-react";
import { useState, type FormEvent } from "react";

type Message = { role: "user" | "assistant"; content: string; model?: string; tokens?: number };
type Props = { model: string; messages: Message[]; unavailable: boolean; onSend: (content: string) => void };

export function ChatPanel({ model, messages, unavailable, onSend }: Props) {
  const [content, setContent] = useState("");
  const submit = (event: FormEvent) => { event.preventDefault(); if (content.trim()) { onSend(content); setContent(""); } };
  return <section className="panel"><div className="page-heading"><div><h2>Exploratory conversation</h2><p className="muted">{model || "Choose a local model"} · local only · evidence review required</p></div></div><div className="transcript">{messages.length ? messages.map((message, index) => <article key={`${message.role}-${index}`} className={`message message--${message.role}`}><strong>{message.role === "user" ? "Researcher" : "Local model"}</strong><div>{message.content}</div>{message.tokens !== undefined && <div className="message-meta">{message.tokens} output tokens · exploratory</div>}</article>) : <p className="muted">Start a local conversation to inspect model behavior. Messages cannot become research evidence automatically.</p>}</div><form className="composer" onSubmit={submit}><input aria-label="Chat message" disabled={unavailable} value={content} onChange={(e) => setContent(e.target.value)} placeholder={unavailable ? "Start Ollama to enable chat" : "Ask the selected local model…"} /><button className="action" aria-label="Send message" disabled={unavailable}><Send size={16} /></button></form></section>;
}