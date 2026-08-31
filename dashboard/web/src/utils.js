export function firstSentence(text) {
  const t = text.trim().replace(/^"+|"+$/g, "").trim();
  const match = t.match(/[.!?]\s/);
  const cut = match ? match.index + 1 : t.length;
  return t.slice(0, cut).trim();
}
