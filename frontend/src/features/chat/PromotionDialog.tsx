type Props = { disabled: boolean };

export function PromotionDialog({ disabled }: Props) {
  return <aside className="panel"><h2>Promote candidate</h2><p className="muted">Promotion requires an explicit provenance, access class, and experiment decision. It is never automatic.</p><button className="action" disabled={disabled}>Review provenance first</button></aside>;
}