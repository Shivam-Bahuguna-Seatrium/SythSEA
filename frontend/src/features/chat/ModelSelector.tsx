import { useQuery } from "@tanstack/react-query";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { StatusBadge } from "../../components/StatusBadge";

export type LocalModel = { model_version: string; available: boolean; unavailable_reason?: string };
type Props = { value: string; onChange: (value: string) => void };

export function ModelSelector({ value, onChange }: Props) {
  const models = useQuery({ queryKey: ["models"], queryFn: () => api<LocalModel[]>(routes.models) });
  const available = models.data?.filter((model) => model.available) ?? [];
  return <aside className="panel"><h2>Local model</h2>{available.length > 0 ? <select value={value} onChange={(e) => onChange(e.target.value)}>{available.map((model) => <option key={model.model_version}>{model.model_version}</option>)}</select> : <><StatusBadge status="unavailable" /><p className="muted">{models.data?.[0]?.unavailable_reason ?? "Checking Ollama service…"}</p></>}<p className="muted">Local only. Chat is exploratory until promoted with provenance review.</p></aside>;
}