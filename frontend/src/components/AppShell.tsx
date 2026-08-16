import { BarChart3, Bot, Database, FlaskConical, Menu, ShieldCheck } from "lucide-react";
import { NavLink } from "react-router-dom";
import type { PropsWithChildren } from "react";

import { StatusBadge } from "./StatusBadge";

const links = [
  ["/", "Overview", BarChart3],
  ["/intake", "Data Intake", Database],
  ["/training", "Fine-Tuning", FlaskConical],
  ["/chat", "Local Chat", Bot],
  ["/evidence", "Evidence", ShieldCheck],
] as const;

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span>Synth</span>SEA</div>
        <nav aria-label="Workbench navigation">
          {links.map(([to, label, Icon]) => (
            <NavLink key={to} to={to} className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              <Icon size={18} /><span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-note">Local research workspace<br />Evidence-aware by design</div>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <button className="icon-button mobile-menu" aria-label="Open navigation" title="Open navigation"><Menu size={18} /></button>
          <div><span className="eyebrow">LOCAL WORKSPACE</span><strong>Apple Silicon Research Node</strong></div>
          <div className="topbar-status"><span>Release</span><StatusBadge status="blocked" /></div>
        </header>
        <main className="content">{children}</main>
      </section>
    </div>
  );
}