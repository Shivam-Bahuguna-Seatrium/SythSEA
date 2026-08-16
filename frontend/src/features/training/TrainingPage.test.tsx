import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { TrainingForm } from "./TrainingForm";
import { TrainingHistory, TrainingJobs } from "./TrainingJobs";

describe("TrainingForm", () => {
  it("submits a declared MLX-LM training engine", () => {
    const submit = vi.fn();
    render(<TrainingForm onSubmit={submit} pending={false} />);

    fireEvent.click(screen.getByRole("button", { name: "Queue MLX-LM job" }));

    expect(submit).toHaveBeenCalledWith(expect.objectContaining({ training_engine: "mlx_lm" }));
  });

  it("explains why a queued job has not started", () => {
    render(<TrainingJobs job={{ job_id: "mlx-123", status: "queued", model_version: "qwen3-8b-synthsea", dataset_version: "fixture:v1", language_slices: ["singlish"], training_command: "mlx_lm.lora", failure_reason: "", unified_memory_mb: 0 }} onCancel={() => undefined} />);

    expect(screen.getByRole("status").textContent).toContain("Waiting for the local MLX-LM worker");
  });

  it("shows a persisted training issue in history", () => {
    render(<TrainingHistory jobs={[{ job_id: "mlx-123", status: "blocked", model_version: "qwen3-8b-synthsea", dataset_version: "fixture:v1", language_slices: ["singlish"], training_command: "mlx_lm.lora", failure_reason: "Apple Silicon is required", unified_memory_mb: 0 }]} />);

    expect(screen.getByText("Apple Silicon is required")).toBeTruthy();
  });
});