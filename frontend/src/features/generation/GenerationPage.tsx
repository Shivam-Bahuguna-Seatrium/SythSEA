import { useMutation } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";

import { api } from "../../api/client";
import { routes } from "../../api/routes";

type Run = { run_id: string; model_version: string; record_count: number; failures: string[]; stages: string[]; artifact_ref: string };

export function GenerationPage() {
  const [topic, setTopic] = useState("Singapore workplace communication");
  const [language, setLanguage] = useState("singlish");
  const [count, setCount] = useState("8");
  const run = useMutation({ mutationFn: () => api<Run>(routes.generationRuns, { method: "POST", body: JSON.stringify({ topic, language_profile_id: language, prompt_count: Number(count), seed: 13, model_version: "gpt-oss:20b" }) }) });
  const submit = (event: FormEvent) => { event.preventDefault(); run.mutate(); };
  return <><section className="page-heading"><div><h1>Data generation</h1><p>Create candidate multilingual instruction data with your local gpt-oss:20b model, then preserve each validation stage for the research pipeline.</p></div></section><section className="grid grid--two"><form className="panel form-grid" onSubmit={submit}><div className="field field--wide"><label>Research topic</label><input value={topic} onChange={(event) => setTopic(event.target.value)} /></div><div className="field"><label>Language slice</label><select value={language} onChange={(event) => setLanguage(event.target.value)}><option value="singlish">Singapore English/Singlish</option><option value="malay">Malay</option><option value="tamil">Tamil</option><option value="singapore_mandarin">Singapore Mandarin</option></select></div><div className="field"><label>Candidate prompts</label><input type="number" min="1" max="100" value={count} onChange={(event) => setCount(event.target.value)} /></div><div className="field field--wide"><p className="muted">Local LLM: gpt-oss:20b. Agent stages record cultural, semantic, diversity, critic, judge, and refinement decisions. Generated text is candidate data, not paper evidence.</p><button className="action" disabled={run.isPending}>{run.isPending ? "Generating..." : "Run multi-agent generation"}</button></div></form><section className="panel"><h2>Methodology path</h2><ol className="methodology-list"><li>Generate candidate data with local GPT-OSS.</li><li>Review/filter and register approved data.</li><li>Fine-tune and compare baselines per language.</li><li>Evaluate, register evidence, then build the research report.</li></ol>{run.data && <><p><strong>{run.data.record_count}</strong> candidate records saved.</p><p className="muted">{run.data.artifact_ref}</p><p className="muted">Stages: {run.data.stages.join(", ")}</p>{run.data.failures.map((failure) => <p className="danger" key={failure}>Issue: {failure}</p>)}</>}{run.error && <p className="danger">{run.error.message}</p>}</section></section></>;
}