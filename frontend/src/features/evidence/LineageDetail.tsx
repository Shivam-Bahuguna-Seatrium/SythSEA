import { useState } from "react";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { StatusBadge } from "../../components/StatusBadge";

type Artifact = { artifact_id: string; access_class: string; validation_status: string; source_refs: string[]; dependent_refs: string[]; limitations: string[] };

export function LineageDetail() {
  const [artifactId, setArtifactId] = useState("fixture-artifact");
  const [artifact, setArtifact] = useState<Artifact | null>(null);
  const [error, setError] = useState("");
  const inspect = async () => { try { setArtifact(await api<Artifact>(routes.lineage(artifactId))); setError(""); } catch (issue) { setError(issue instanceof Error ? issue.message : "Unable to load lineage"); } };
  return <section className="panel"><h2>Artifact lineage</h2><div className="composer"><input aria-label="Artifact identifier" value={artifactId} onChange={(e) => setArtifactId(e.target.value)} /><button className="action" type="button" onClick={inspect}>Inspect</button></div>{error && <p className="danger">{error}</p>}{artifact && <div><p><StatusBadge status={artifact.validation_status} /> <span className="muted">{artifact.access_class}</span></p><p><strong>Sources:</strong> {artifact.source_refs.join(", ")}</p><p><strong>Dependents:</strong> {artifact.dependent_refs.join(", ") || "None recorded"}</p><p className="muted">{artifact.limitations.join(" ")}</p></div>}</section>;
}