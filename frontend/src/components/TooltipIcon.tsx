import type { LucideIcon } from "lucide-react";

type Props = { icon: LucideIcon; label: string; onClick?: () => void };

export function TooltipIcon({ icon: Icon, label, onClick }: Props) {
  return (
    <button className="icon-button" type="button" aria-label={label} title={label} onClick={onClick}>
      <Icon size={17} />
    </button>
  );
}