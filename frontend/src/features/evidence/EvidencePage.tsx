import { useQuery } from "@tanstack/react-query";

import { api } from "../../api/client";
import { routes } from "../../api/routes";
import { LineageDetail } from "./LineageDetail";
import { ReadinessPanel } from "./ReadinessPanel";

type Readiness = { releaseStatus: string; items: { item_id: string; message: string; severity: string }[] };

export function EvidencePage() {
  const readiness = useQuery({ queryKey: ["readiness"], queryFn: () => api<Readiness>(routes.readiness) });
  return <><section className="page-heading"><div><h1>Evidence and provenance</h1><p>Trace source artifacts, review language-specific coverage, and expose blockers before any report claim is released.</p></div></section><section className="grid grid--two"><ReadinessPanel releaseStatus={readiness.data?.releaseStatus ?? "loading"} items={readiness.data?.items ?? []} /><LineageDetail /></section>{readiness.error && <p className="danger">{readiness.error.message}</p>}</>;
}