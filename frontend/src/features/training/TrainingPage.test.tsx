import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { TrainingForm } from "./TrainingForm";

describe("TrainingForm", () => {
  it("submits a declared MLX-LM training engine", () => {
    const submit = vi.fn();
    render(<TrainingForm onSubmit={submit} pending={false} />);

    fireEvent.click(screen.getByRole("button", { name: "Queue MLX-LM job" }));

    expect(submit).toHaveBeenCalledWith(expect.objectContaining({ training_engine: "mlx_lm" }));
  });
});