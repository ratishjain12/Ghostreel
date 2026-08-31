import { useEffect, useCallback, useState, useRef } from "react";
import { api } from "./api";
import { useJobRunner } from "./hooks/useJobRunner";
import ScriptsPanel from "./components/ScriptsPanel";
import JobLog from "./components/JobLog";
import VideosPanel from "./components/VideosPanel";
import Toast from "./components/Toast";

export default function App() {
  const [scripts, setScripts] = useState([]);
  const [videos, setVideos] = useState([]);
  const [batchTotal, setBatchTotal] = useState(null);
  const [toast, setToast] = useState(null);
  const toastTimer = useRef(null);
  const job = useJobRunner();

  const showToast = useCallback((kind, text) => {
    clearTimeout(toastTimer.current);
    setToast({ kind, text });
    toastTimer.current = setTimeout(() => setToast(null), 5000);
  }, []);

  const loadScripts = useCallback(() => api.listScripts().then(setScripts), []);
  const loadVideos = useCallback(() => api.listVideos().then(setVideos), []);

  useEffect(() => {
    loadScripts();
    loadVideos();
  }, [loadScripts, loadVideos]);

  async function handleGenerate(names) {
    setBatchTotal(names ? names.length : scripts.length);
    await job.run(() => api.generate(names));
    loadScripts();
  }

  async function handleRender(name) {
    setBatchTotal(null);
    await job.run(() => api.render(name));
    loadVideos();
  }

  async function handleAuthor(name) {
    setBatchTotal(null);
    await job.run(() => api.author(name));
    loadScripts();
    loadVideos();
  }

  async function handleGeneratePdf(name) {
    setBatchTotal(null);
    const pdfResult = await job.run(() => api.generatePdf(name));
    loadScripts();
    if (pdfResult?.status !== "done") return; // don't upload a guide that failed to generate
    await job.run(() => api.upload(name));
    loadScripts();
  }

  async function handleSetTrigger(name, mediaId, keyword) {
    setBatchTotal(null);
    await job.run(() => api.setTrigger(name, mediaId, keyword));
    loadScripts();
  }

  async function handlePublish(name, caption, keyword) {
    setBatchTotal(null);
    const result = await job.run(() => api.publish(name, caption, keyword));
    loadScripts();
    if (result?.status === "done") {
      showToast("done", `Posted "${name}" to Instagram${keyword ? ` — trigger "${keyword}" registered` : ""}.`);
    } else if (result?.status === "error") {
      showToast("error", `Publishing "${name}" failed — check the job log.`);
    }
  }

  const signalState = job.status === "running" ? "running" : job.status === "done" ? "done" : job.status === "error" ? "error" : "idle";

  return (
    <>
      <header className="masthead">
        <div className="masthead-title">
          <h1>Reel Pipeline</h1>
          <span className="sub">script → voice → captions → render</span>
        </div>
        <div className={`signal ${signalState}`}>
          <span className="lamp" />
          {signalState}
        </div>
      </header>
      <main>
        <ScriptsPanel
          scripts={scripts}
          onChanged={loadScripts}
          onGenerate={handleGenerate}
          onAuthor={handleAuthor}
          onRender={handleRender}
          onGeneratePdf={handleGeneratePdf}
          onSetTrigger={handleSetTrigger}
          onPublish={handlePublish}
        />
        <div className="side-stack">
          <JobLog status={job.status} lines={job.lines} total={batchTotal} />
          <VideosPanel projects={videos} onRefresh={loadVideos} />
        </div>
      </main>
      <Toast toast={toast} onDismiss={() => setToast(null)} />
    </>
  );
}
