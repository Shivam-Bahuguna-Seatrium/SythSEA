import { Ban, FileText } from "lucide-react";

import { StatusBadge } from "../../components/StatusBadge";
import { TooltipIcon } from "../../components/TooltipIcon";

export type Job = { job_id: string; status: string; model_version: string; dataset_version: string; language_slices: string[]; training_command: string; failure_reason: string; unified_memory_mb: number };

type Props = { job: Job | null; onCancel: () => void };

function statusExplanation(job: Job): string {
  if (job.status === "queued") return "Waiting for the local MLX-LM worker to start. If this remains queued for more than 10 seconds, restart the FastAPI server and review its terminal output.";
  if (job.status === "running") return "MLX-LM is downloading the model if needed, then training the adapter. Keep the local server running and do not close the terminal.";
  if (job.status === "succeeded") return "Training completed. Open Local Chat and select Fine-tuned models to test the recorded adapter.";
  if (job.status === "blocked") return "Training cannot start on this workstation. Review the issue below and correct the local requirement before submitting a new job.";
  if (job.status === "failed") return "MLX-LM stopped during execution. Review the issue below and the job log before retrying.";
  if (job.status === "cancelled") return "Training was cancelled before an adapter could be registered.";
  return "Training status is being recorded by the local workspace.";
}

export function TrainingJobs({ job, onCancel }: Props) {
  if (!job) return <aside className="panel empty-state">Submit a job to see MLX-LM command, status, checkpoint artifacts, and resource metadata.</aside>;
  return <aside className="panel"><div className="page-heading"><div><h2>Latest job</h2><p className="muted">{job.job_id}</p></div><StatusBadge status={job.status} /></div><p className="job-status" role="status">{statusExplanation(job)}</p><table className="table"><tbody><tr><th>Model</th><td>{job.model_version}</td></tr><tr><th>Dataset</th><td>{job.dataset_version}</td></tr><tr><th>Slice</th><td>{job.language_slices.join(", ")}</td></tr><tr><th>Memory</th><td>{job.unified_memory_mb || "not recorded"} MB</td></tr></tbody></table><p className="muted"><FileText size={14} /> {job.training_command}</p>{job.failure_reason && <p className="danger"><strong>Issue:</strong> {job.failure_reason}</p>}{["queued", "running"].includes(job.status) && <TooltipIcon icon={Ban} label="Cancel training job" onClick={onCancel} />}</aside>;
}

export function TrainingHistory({ jobs }: { jobs: Job[] }) {
  return <section className="panel training-history"><div className="page-heading"><div><h2>Training history</h2><p className="muted">Stored locally in the workspace job records.</p></div></div>{jobs.length ? <table className="table"><thead><tr><th>Job</th><th>Model</th><th>Status</th><th>Issue</th></tr></thead><tbody>{jobs.map((job) => <tr key={job.job_id}><td>{job.job_id}</td><td>{job.model_version}</td><td><StatusBadge status={job.status} /></td><td>{job.failure_reason || "-"}</td></tr>)}</tbody></table> : <p className="muted">No local training jobs have been recorded.</p>}</section>;
}