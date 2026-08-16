import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { TrainingForm } from "./TrainingForm";
import { TrainingJobs, type Job } from "./TrainingJobs";

export function TrainingPage() {
  const [job, setJob] = useState<Job | null>(null);
  const submit = useMutation({ mutationFn: (body: unknown) => api<Job>(routes.jobs, { method: "POST", body: JSON.stringify(body) }), onSuccess: setJob });
  const status = useQuery({ queryKey: ["training-job", job?.job_id], queryFn: () => api<Job>(`${routes.jobs}/${job?.job_id}`), enabled: Boolean(job), refetchInterval: (query) => ["queued", "running"].includes(query.state.data?.status ?? job?.status ?? "") ? 1000 : false });
  const displayedJob = status.data ?? job;
  const cancel = useMutation({ mutationFn: () => displayedJob ? api<Job>(`${routes.jobs}/${displayedJob.job_id}`, { method: "DELETE" }) : Promise.reject(new Error("No job selected")), onSuccess: setJob });
  return <><section className="page-heading"><div><h1>Fine-tuning</h1><p>Submit MLX-LM jobs with the full training command, model license, seed, dataset split, and Apple Silicon memory context.</p></div></section><section className="grid grid--two"><TrainingForm pending={submit.isPending} onSubmit={(body) => submit.mutate(body)} /><TrainingJobs job={displayedJob} onCancel={() => cancel.mutate()} /></section>{(submit.error || status.error || cancel.error) && <p className="danger">{(submit.error ?? status.error ?? cancel.error)?.message}</p>}</>;
}