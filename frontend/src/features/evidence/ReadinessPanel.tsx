import { AlertTriangle } from "lucide-react";

import { StatusBadge } from "../../components/StatusBadge";

type Props = { releaseStatus: string; items: { item_id: string; message: string; severity: string }[] };

export function ReadinessPanel({ releaseStatus, items }: Props) {
  return <section className="panel"><div className="page-heading"><div><h2>Research readiness</h2><p className="muted">Publication release stays blocked until all evidence and governance checks resolve.</p></div><StatusBadge status={releaseStatus} /></div>{items.length > 0 ? <ul className="issue-list">{items.map((item) => <li key={item.item_id}><AlertTriangle size={14} /> {item.message}</li>)}</ul> : <p className="muted">No readiness issues returned.</p>}<table className="table"><thead><tr><th>Language slice</th><th>Evidence state</th></tr></thead><tbody>{["Singapore English/Singlish", "Malay", "Tamil", "Singapore Mandarin"].map((slice) => <tr key={slice}><td>{slice}</td><td><StatusBadge status="missing" /></td></tr>)}</tbody></table></section>;
}