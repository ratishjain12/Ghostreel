import { useState } from "react";
import ScriptForm from "./ScriptForm";

const EMPTY = { name: "", text: "", message: "", aspect: "" };

export default function NewScriptForm({ onCreated }) {
  const [open, setOpen] = useState(false);
  const [resetKey, setResetKey] = useState(0);

  return (
    <details className="new-script" open={open} onToggle={(e) => setOpen(e.target.open)}>
      <summary>Add script</summary>
      <ScriptForm
        key={resetKey}
        initial={EMPTY}
        submitLabel="Save script"
        onDone={() => {
          setOpen(false);
          setResetKey((k) => k + 1);
          onCreated();
        }}
      />
    </details>
  );
}
