import { useState, type FormEvent } from "react";

type Props = { onSubmit: (dataset: Record<string, unknown>, recordSource: string) => void; pending: boolean };

const initial = { dataset_id: "", dataset_version: "v1", source_uri_or_reference: "", provenance: "", license: "", permitted_use: "research", access_class: "public", retention_rule: "project", language_profile_id: "singlish", acquisition_method: "researcher_registered", content_hash: "pending", record_count: 0, status: "eligible" };

export function DatasetIntakeForm({ onSubmit, pending }: Props) {
  const [dataset, setDataset] = useState(initial);
  const [recordSource, setRecordSource] = useState("fixtures/dataset.json");
  const update = (field: keyof typeof initial, value: string | number) => setDataset({ ...dataset, [field]: value });
  const submit = (event: FormEvent) => { event.preventDefault(); onSubmit(dataset, recordSource); };
  return <form className="panel form-grid" onSubmit={submit}>
    <div className="field"><label htmlFor="dataset-id">Dataset ID</label><input id="dataset-id" value={dataset.dataset_id} onChange={(e) => update("dataset_id", e.target.value)} required /></div>
    <div className="field"><label htmlFor="dataset-version">Version</label><input id="dataset-version" value={dataset.dataset_version} onChange={(e) => update("dataset_version", e.target.value)} required /></div>
    <div className="field field--wide"><label htmlFor="source">Source reference</label><input id="source" value={dataset.source_uri_or_reference} onChange={(e) => update("source_uri_or_reference", e.target.value)} required /></div>
    <div className="field"><label htmlFor="provenance">Provenance</label><input id="provenance" value={dataset.provenance} onChange={(e) => update("provenance", e.target.value)} required /></div>
    <div className="field"><label htmlFor="license">License</label><input id="license" value={dataset.license} onChange={(e) => update("license", e.target.value)} required /></div>
    <div className="field"><label htmlFor="language">Language profile</label><select id="language" value={dataset.language_profile_id} onChange={(e) => update("language_profile_id", e.target.value)}><option value="singlish">Singapore English/Singlish</option><option value="malay">Malay</option><option value="tamil">Tamil</option><option value="singapore_mandarin">Singapore Mandarin</option></select></div>
    <div className="field"><label htmlFor="access">Access class</label><select id="access" value={dataset.access_class} onChange={(e) => update("access_class", e.target.value)}><option value="public">Public</option><option value="restricted">Restricted</option><option value="private">Private</option></select></div>
    <div className="field"><label htmlFor="retention">Retention rule</label><input id="retention" value={dataset.retention_rule} onChange={(e) => update("retention_rule", e.target.value)} required /></div>
    <div className="field"><label htmlFor="record-source">Record source</label><input id="record-source" value={recordSource} onChange={(e) => setRecordSource(e.target.value)} required /></div>
    <div className="field field--wide"><button className="action" disabled={pending} type="submit">{pending ? "Validating…" : "Validate dataset intake"}</button></div>
  </form>;
}