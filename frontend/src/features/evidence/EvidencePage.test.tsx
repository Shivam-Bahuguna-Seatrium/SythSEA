import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ReadinessPanel } from "./ReadinessPanel";

describe("ReadinessPanel", () => {
  it("shows blocked readiness and separate target language slices", () => {
    render(<ReadinessPanel releaseStatus="blocked" items={[{ item_id: "one", message: "venue_not_approved", severity: "blocking" }]} />);

    expect(screen.getByText("venue_not_approved")).toBeInTheDocument();
    expect(screen.getByText("Singapore English/Singlish")).toBeInTheDocument();
    expect(screen.getByText("Singapore Mandarin")).toBeInTheDocument();
  });
});