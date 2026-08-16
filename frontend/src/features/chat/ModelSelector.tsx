import { useQuery } from "@tanstack/react-query";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { StatusBadge } from "../../components/StatusBadge";

export type LocalModel = { model_version: string; available: boolean; engine: "ollama" | "mlx_lm"; unavailable_reason?: string };
type Props = { value: string; engine: "ollama" | "mlx_lm"; onChange: (value: string) => void };

export function ModelSelector({ value, engine, onChange }: Props) {
  const models = useQuery({ queryKey: ["models"], queryFn: () => api<LocalModel[]>(routes.models) });
  const candidates = models.data?.filter((model) => model.engine === engine) ?? [];
  const available = candidates.filter((model) => model.available);
  const unavailableReason = candidates[0]?.unavailable_reason ?? (engine === "mlx_lm" ? "Complete a fine-tuning job on macOS to enable this tab." : "Checking Ollama service…");
  return <aside className="panel"><h2>{engine === "mlx_lm" ? "Fine-tuned model" : "Ollama model"}</h2>{available.length > 0 ? <select value={value} onChange={(e) => onChange(e.target.value)}>{available.map((model) => <option key={model.model_version}>{model.model_version}</option>)}</select> : <><StatusBadge status="unavailable" /><p className="muted">{unavailableReason}</p></>}<p className="muted">Local only. Chat is exploratory until promoted with provenance review.</p></aside>;
}