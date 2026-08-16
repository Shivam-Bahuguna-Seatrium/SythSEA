import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { DatasetIntakeForm } from "./DatasetIntakeForm";
import { IntakeResult } from "./IntakeResult";

type Result = { intake_id: string; validation_status: string; issues: string[]; lineage_artifact_id?: string };

export function DatasetIntakePage() {
  const [result, setResult] = useState<Result | null>(null);
  const intake = useMutation({ mutationFn: (body: unknown) => api<Result>(routes.intake, { method: "POST", body: JSON.stringify(body) }), onSuccess: setResult });
  return <><section className="page-heading"><div><h1>Data intake</h1><p>Register source data only after its provenance, license, retention, language profile, and access class are known.</p></div></section><section className="grid grid--two"><DatasetIntakeForm pending={intake.isPending} onSubmit={(dataset, recordSource) => intake.mutate({ dataset, record_source: recordSource })} />{result ? <IntakeResult result={result} /> : <aside className="panel empty-state">Submit a dataset intake to see an eligible, restricted, or blocked decision.</aside>}</section>{intake.error && <p className="danger">{intake.error.message}</p>}</>;
}