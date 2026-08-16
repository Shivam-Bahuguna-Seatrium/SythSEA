type Props = { status: string };

export function StatusBadge({ status }: Props) {
  return <span className={`status status--${status}`}>{status.replaceAll("_", " ")}</span>;
}