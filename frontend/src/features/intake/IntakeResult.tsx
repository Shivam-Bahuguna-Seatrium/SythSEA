import { Link } from "react-router-dom";
import { StatusBadge } from "../../components/StatusBadge";

type Props = { result: { intake_id: string; validation_status: string; issues: string[]; lineage_artifact_id?: string } };

export function IntakeResult({ result }: Props) {
  return <aside className="panel"><h2>Validation outcome</h2><StatusBadge status={result.validation_status} /><p className="muted">Intake {result.intake_id}</p>{result.issues.length > 0 && <ul className="issue-list">{result.issues.map((issue) => <li key={issue}>{issue}</li>)}</ul>}{result.lineage_artifact_id && <Link to="/evidence">Open artifact lineage</Link>}</aside>;
}