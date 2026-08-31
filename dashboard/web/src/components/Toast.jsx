export default function Toast({ toast, onDismiss }) {
  if (!toast) return null;
  return (
    <div className={`toast ${toast.kind}`} role="status">
      <span>{toast.text}</span>
      <button className="toast-close" onClick={onDismiss} aria-label="Dismiss">
        ×
      </button>
    </div>
  );
}
