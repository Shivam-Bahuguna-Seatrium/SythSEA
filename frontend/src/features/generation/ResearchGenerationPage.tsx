import { useMutation, useQuery } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";

import { api } from "../../api/client";
import { routes } from "../../api/routes";

type QualityReport = {
  total_candidates?: number;
  generation_failures?: number;
  incomplete_records?: number;
  exact_duplicate_records?: number;
  unique_pair_rate?: number;
  mean_response_tokens?: number;
  automated_audit?: string;
  downstream_benchmark?: string;
};

type Run = {
  run_id: string;
  dataset_version: string;
  language_profile_id: string;
  dataset_path: string;
  model_version: string;
  record_count: number;
  requested_count: number;
  status: string;
  evaluation_status: string;
  benchmark_status: string;
  quality_report: QualityReport;
  failures: string[];
  stages: string[];
  records: { instruction: string; response: string }[];
};

const taskFamilies = [
  "workplace pragmatics",
  "cultural explanation",
  "code-switching",
  "safety-aware clarification",
];

const studyGates = [
  "Frozen external or pre-generation held-out test set",
  "Base, seed-only, and unfiltered-synthetic baselines",
  "Ablations for critic/judge, diversity, and language-specialist stages",
  "Three seeds, per-language reporting, confidence intervals, and data-efficiency curve",
  "Stratified human review by task family and language slice",
];

export function ResearchGenerationPage() {
  const [topic, setTopic] = useState("Singapore workplace communication");
  const [language, setLanguage] = useState("singlish");
  const [count, setCount] = useState("8");
  const createRun = useMutation({
    mutationFn: () => api<Run>(routes.generationRuns, {
      method: "POST",
      body: JSON.stringify({
        topic,
          language_profile_id: language,
        prompt_count: Number(count),
        seed: 13,
        model_version: "gpt-oss:20b",
      }),
    }),
  });
  const auditRun = useMutation({
    mutationFn: (runId: string) => api<Run>(`${routes.generationRuns}/${runId}/evaluate`, {
      method: "POST",
    }),
  });
  const activeRun = useQuery({
    queryKey: ["generation-run", createRun.data?.run_id],
    queryFn: () => api<Run>(`${routes.generationRuns}/${createRun.data?.run_id}`),
    enabled: Boolean(createRun.data),
    refetchInterval: (query) => (
      ["queued", "running"].includes(query.state.data?.status ?? createRun.data?.status ?? "")
        ? 1000
        : false
    ),
  });
  const history = useQuery({
    queryKey: ["generation-history"],
    queryFn: () => api<Run[]>(routes.generationRuns),
    refetchInterval: 2000,
  });
  const displayed = auditRun.data ?? activeRun.data ?? createRun.data;
  const error = createRun.error ?? auditRun.error ?? activeRun.error ?? history.error;

  function submit(event: FormEvent) {
    event.preventDefault();
    createRun.mutate();
  }

  return <>
    <section className="page-heading">
      <div>
        <h1>Synthetic Data Study</h1>
        <p>Controlled instruction-data generation with auditable quality gates and downstream benchmark requirements.</p>
      </div>
    </section>

    <section className="grid grid--two">
      <form className="panel form-grid" onSubmit={submit}>
        <div className="field field--wide">
          <label>Research question</label>
          <p className="muted">Does curated multi-agent synthetic data improve held-out performance over unfiltered and seed-only instruction data?</p>
        </div>
        <div className="field field--wide">
          <label>Research topic</label>
          <input value={topic} onChange={(event) => setTopic(event.target.value)} />
        </div>
        <div className="field">
          <label>Language slice</label>
          <select value={language} onChange={(event) => setLanguage(event.target.value)}>
            <option value="singlish">Singapore English/Singlish</option>
            <option value="malay">Malay</option>
            <option value="tamil">Tamil</option>
            <option value="singapore_mandarin">Singapore Mandarin</option>
          </select>
        </div>
        <div className="field">
          <label>Candidate prompts</label>
          <input type="number" min="1" max="100" value={count} onChange={(event) => setCount(event.target.value)} />
        </div>
        <div className="field field--wide">
          <label>Prompt families</label>
          <p className="muted">{taskFamilies.join(" | ")}</p>
        </div>
        <div className="field field--wide">
          <p className="muted">Generator: local gpt-oss:20b, seed 13. The output is candidate data, never evidence of model improvement.</p>
          <button className="action" disabled={createRun.isPending}>
            {createRun.isPending ? "Starting study run..." : "Generate candidate batch"}
          </button>
        </div>
      </form>

      <section className="panel">
        <h2>Study Protocol</h2>
        <ol className="methodology-list">
          {studyGates.map((gate) => <li key={gate}>{gate}</li>)}
        </ol>
        <p className="muted">A completed audit permits training intake. It does not establish a paper claim.</p>
      </section>
    </section>

    <section className="grid grid--two training-history">
      <section className="panel">
        <h2>Candidate Batch</h2>
        {displayed ? <>
          <p><strong>{displayed.status}</strong>: {displayed.record_count} of {displayed.requested_count} records persisted.</p>
          <p className="muted">{displayed.dataset_version} | {displayed.model_version}</p>
          <p className="muted">Audit: {displayed.evaluation_status} | Benchmark: {displayed.benchmark_status}</p>
          <p className="muted">Candidate-data path: {displayed.dataset_path}/train.jsonl</p>
          {displayed.status === "completed" && displayed.evaluation_status === "not_started" && <button className="action" onClick={() => auditRun.mutate(displayed.run_id)} disabled={auditRun.isPending}>Run automatic data audit</button>}
          {displayed.failures.map((failure) => <p className="danger" key={failure}>Issue: {failure}</p>)}
        </> : <p className="muted">Create a batch to record its candidate-data lineage.</p>}
      </section>

      <section className="panel">
        <h2>Audit Evidence</h2>
        {displayed?.quality_report?.total_candidates !== undefined ? <table className="table">
          <tbody>
            <tr><th>Candidate records</th><td>{displayed.quality_report.total_candidates}</td></tr>
            <tr><th>Exact duplicates</th><td>{displayed.quality_report.exact_duplicate_records}</td></tr>
            <tr><th>Incomplete records</th><td>{displayed.quality_report.incomplete_records}</td></tr>
            <tr><th>Unique-pair rate</th><td>{((displayed.quality_report.unique_pair_rate ?? 0) * 100).toFixed(1)}%</td></tr>
            <tr><th>Mean response tokens</th><td>{(displayed.quality_report.mean_response_tokens ?? 0).toFixed(1)}</td></tr>
          </tbody>
        </table> : <p className="muted">Run the automatic audit after generation to record duplicate, completeness, and response-length evidence.</p>}
      </section>
    </section>

    <section className="panel training-history">
      <h2>Generated Dataset Versions</h2>
      <table className="table">
        <thead><tr><th>Version</th><th>Slice</th><th>Records</th><th>Audit</th><th>Benchmark state</th></tr></thead>
        <tbody>{(history.data ?? []).map((batch) => <tr key={batch.run_id}>
          <td>{batch.dataset_version}</td><td>{batch.language_profile_id}</td>
          <td>{batch.record_count}/{batch.requested_count}</td><td>{batch.evaluation_status}</td><td>{batch.benchmark_status}</td>
        </tr>)}</tbody>
      </table>
    </section>

    {error && <p className="danger">{error.message}</p>}
  </>;
}