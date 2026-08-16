import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { ChatPanel } from "./ChatPanel";
import { ModelSelector } from "./ModelSelector";
import { PromotionDialog } from "./PromotionDialog";

type Conversation = { conversation_id: string; status: string; model_version: string };
type Message = { role: "user" | "assistant"; content: string; model?: string; tokens?: number };

export function ChatPage() {
  const [model, setModel] = useState("");
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const create = useMutation({ mutationFn: (modelVersion: string) => api<Conversation>(routes.conversations, { method: "POST", body: JSON.stringify({ model_version: modelVersion, access_class: "private" }) }), onSuccess: setConversation });
  const send = useMutation({ mutationFn: (content: string) => conversation ? api<{ content: string; output_tokens: number; model_version: string }>(`${routes.conversations}/${conversation.conversation_id}/messages`, { method: "POST", body: JSON.stringify({ content }) }) : Promise.reject(new Error("Select an available model first")), onSuccess: (response, content) => setMessages((current) => [...current, { role: "user", content }, { role: "assistant", content: response.content, model: response.model_version, tokens: response.output_tokens }]) });
  const chooseModel = (next: string) => { setModel(next); setMessages([]); create.mutate(next); };
  return <><section className="page-heading"><div><h1>Local chat</h1><p>Inspect a local Ollama model without promoting conversation text into a dataset or research claim.</p></div></section><section className="chat-layout"><div className="grid"><ModelSelector value={model} onChange={chooseModel} /><PromotionDialog disabled /></div><ChatPanel model={model} messages={messages} unavailable={!conversation || conversation.status !== "active" || send.isPending} onSend={(content) => send.mutate(content)} /></section>{(create.error || send.error) && <p className="danger">{(create.error ?? send.error)?.message}</p>}</>;
}