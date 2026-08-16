import { Ban, FileText } from "lucide-react";

import { StatusBadge } from "../../components/StatusBadge";
import { TooltipIcon } from "../../components/TooltipIcon";

export type Job = { job_id: string; status: string; model_version: string; dataset_version: string; language_slices: string[]; training_command: string; failure_reason: string; unified_memory_mb: number };

type Props = { job: Job | null; onCancel: () => void };

export function TrainingJobs({ job, onCancel }: Props) {
  if (!job) return <aside className="panel empty-state">Submit a job to see MLX-LM command, status, checkpoint artifacts, and resource metadata.</aside>;
  return <aside className="panel"><div className="page-heading"><div><h2>Latest job</h2><p className="muted">{job.job_id}</p></div><StatusBadge status={job.status} /></div><table className="table"><tbody><tr><th>Model</th><td>{job.model_version}</td></tr><tr><th>Dataset</th><td>{job.dataset_version}</td></tr><tr><th>Slice</th><td>{job.language_slices.join(", ")}</td></tr><tr><th>Memory</th><td>{job.unified_memory_mb || "not recorded"} MB</td></tr></tbody></table><p className="muted"><FileText size={14} /> {job.training_command}</p>{job.failure_reason && <p className="danger">{job.failure_reason}</p>}{["queued", "running"].includes(job.status) && <TooltipIcon icon={Ban} label="Cancel training job" onClick={onCancel} />}</aside>;
}