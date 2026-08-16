import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ChatPanel } from "./ChatPanel";

describe("ChatPanel", () => {
  it("labels unavailable local inference clearly", () => {
    render(<ChatPanel model="" messages={[]} unavailable onSend={() => undefined} />);

    expect(screen.getByPlaceholderText("Start Ollama to enable chat")).toBeDisabled();
    expect(screen.getByText(/cannot become research evidence automatically/i)).toBeInTheDocument();
  });
});