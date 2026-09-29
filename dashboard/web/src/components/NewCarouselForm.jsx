import { useState } from "react";
import CarouselForm from "./CarouselForm";

const EMPTY = { name: "", text: "", message: "", slide_count: 6, pillar: "", hook_style: "" };

export default function NewCarouselForm({ onCreated }) {
  const [open, setOpen] = useState(false);
  const [resetKey, setResetKey] = useState(0);

  return (
    <details className="new-script" open={open} onToggle={(e) => setOpen(e.target.open)}>
      <summary>Add carousel</summary>
      <CarouselForm
        key={resetKey}
        initial={EMPTY}
        submitLabel="Save carousel"
        onDone={() => {
          setOpen(false);
          setResetKey((k) => k + 1);
          onCreated();
        }}
      />
    </details>
  );
}
