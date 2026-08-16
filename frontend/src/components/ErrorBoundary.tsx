import { Component, type ReactNode } from "react";

type Props = { children: ReactNode };
type State = { failed: boolean };

export class ErrorBoundary extends Component<Props, State> {
  state: State = { failed: false };

  static getDerivedStateFromError(): State {
    return { failed: true };
  }

  componentDidCatch(): void {}

  render(): ReactNode {
    if (this.state.failed) {
      return <main className="panel empty-state">Workbench view failed to load. Refresh to retry.</main>;
    }
    return this.props.children;
  }
}