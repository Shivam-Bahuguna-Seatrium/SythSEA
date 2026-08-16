import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Database, FlaskConical, ShieldAlert } from "lucide-react";
import { Link } from "react-router-dom";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { StatusBadge } from "../../components/StatusBadge";

type Readiness = { releaseStatus: string; items: { message: string }[] };

export function OverviewPage() {
  const readiness = useQuery({ queryKey: ["readiness"], queryFn: () => api<Readiness>(routes.readiness) });
  const blockers = readiness.data?.items ?? [];
  return (
    <>
      <section className="page-heading"><div><h1>Research control room</h1><p>Governed intake, reproducible MLX-LM jobs, and exploratory local chat in one local workspace.</p></div><StatusBadge status={readiness.data?.releaseStatus ?? "loading"} /></section>
      <section className="grid grid--three">
        <article className="panel"><Database color="#1e6a46" /><p className="metric">Data intake</p><p className="muted">Validate provenance before generation or training.</p><Link to="/intake">Open intake <ArrowRight size={14} /></Link></article>
        <article className="panel"><FlaskConical color="#aa6b00" /><p className="metric">MLX-LM jobs</p><p className="muted">Track local Apple Silicon fine-tuning as auditable work.</p><Link to="/training">Open jobs <ArrowRight size={14} /></Link></article>
        <article className="panel"><ShieldAlert color="#b9442b" /><p className="metric">{blockers.length}</p><p className="muted">Current report-readiness blockers.</p><Link to="/evidence">Review evidence <ArrowRight size={14} /></Link></article>
      </section>
      <section className="panel" style={{ marginTop: 16 }}><h2>Release guardrails</h2>{blockers.length ? <ul className="issue-list">{blockers.slice(0, 5).map((item) => <li key={item.message}>{item.message}</li>)}</ul> : <p className="muted">Loading research readiness.</p>}</section>
    </>
  );
}