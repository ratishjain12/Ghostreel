// Mirrors PILLARS / HOOK_STYLES in dashboard/server.py — keep both in sync.
export const PILLARS = [
  { value: "ai-engineering", label: "AI Engineering" },
  { value: "system-design", label: "System Design" },
  { value: "dev-lessons", label: "Dev Lessons" },
  { value: "ai-news", label: "AI News" },
  { value: "engineering-opinions", label: "Engineering Opinions" },
];

export const HOOK_STYLES = [
  { value: "bold-claim", label: "Bold claim" },
  { value: "question", label: "Question" },
  { value: "number-promise", label: "Number + promise" },
  { value: "contrarian", label: "Contrarian" },
  { value: "before-after", label: "Before/after" },
];

const PILLAR_LABELS = Object.fromEntries(PILLARS.map((p) => [p.value, p.label]));
const HOOK_STYLE_LABELS = Object.fromEntries(HOOK_STYLES.map((h) => [h.value, h.label]));

export function pillarLabel(value) {
  return (value && PILLAR_LABELS[value]) || null;
}

export function hookStyleLabel(value) {
  return (value && HOOK_STYLE_LABELS[value]) || null;
}
