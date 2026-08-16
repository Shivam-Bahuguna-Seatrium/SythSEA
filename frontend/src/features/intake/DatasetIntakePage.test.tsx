import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { DatasetIntakeForm } from "./DatasetIntakeForm";

describe("DatasetIntakeForm", () => {
  it("submits governed dataset metadata", () => {
    const submit = vi.fn();
    render(<DatasetIntakeForm onSubmit={submit} pending={false} />);

    fireEvent.change(screen.getByLabelText("Dataset ID"), { target: { value: "research-v1" } });
    fireEvent.change(screen.getByLabelText("Source reference"), { target: { value: "source://research" } });
    fireEvent.change(screen.getByLabelText("Provenance"), { target: { value: "curated" } });
    fireEvent.change(screen.getByLabelText("License"), { target: { value: "CC-BY-4.0" } });
    fireEvent.click(screen.getByRole("button", { name: "Validate dataset intake" }));

    expect(submit).toHaveBeenCalledOnce();
  });
});