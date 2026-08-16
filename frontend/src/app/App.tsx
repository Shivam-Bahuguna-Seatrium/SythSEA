import { BrowserRouter } from "react-router-dom";

import { AppShell } from "../components/AppShell";
import { ErrorBoundary } from "../components/ErrorBoundary";
import { WorkbenchRoutes } from "./routes";

export function App() {
  return <BrowserRouter><ErrorBoundary><AppShell><WorkbenchRoutes /></AppShell></ErrorBoundary></BrowserRouter>;
}