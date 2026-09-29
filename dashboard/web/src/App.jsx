import { useEffect, useCallback, useState, useRef } from "react";
import { api } from "./api";
import { useJobRunner } from "./hooks/useJobRunner";
import ScriptsPanel from "./components/ScriptsPanel";
import JobLog from "./components/JobLog";
import VideosPanel from "./components/VideosPanel";
import SchedulePanel from "./components/SchedulePanel";
import PerformancePanel from "./components/PerformancePanel";
import CarouselPanel from "./components/CarouselPanel";
import Toast from "./components/Toast";

export default function App() {
  const [view, setView] = useState("pipeline");
  const [scripts, setScripts] = useState([]);
  const [videos, setVideos] = useState([]);
  const [carousels, setCarousels] = useState([]);
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
  const loadCarousels = useCallback(() => api.listCarousels().then(setCarousels), []);

  useEffect(() => {
    loadScripts();
    loadVideos();
    loadCarousels();
  }, [loadScripts, loadVideos, loadCarousels]);

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

  async function handleGenerateCarousel(names) {
    setBatchTotal(names ? names.length : carousels.length);
    await job.run(() => api.generateCarousel(names));
    loadCarousels();
  }

  async function handleAuthorCarousel(name) {
    setBatchTotal(null);
    await job.run(() => api.authorCarousel(name));
    loadCarousels();
  }

  const signalState = job.status === "running" ? "running" : job.status === "done" ? "done" : job.status === "error" ? "error" : "idle";

  return (
    <>
      <header className="masthead">
        <div className="masthead-title">
          <h1>Content Studio</h1>
        </div>
        <nav className="tabs">
          <button className={`tab ${view === "pipeline" ? "active" : ""}`} onClick={() => setView("pipeline")}>
            Pipeline
          </button>
          <button className={`tab ${view === "carousel" ? "active" : ""}`} onClick={() => setView("carousel")}>
            Carousel
          </button>
          <button className={`tab ${view === "schedule" ? "active" : ""}`} onClick={() => setView("schedule")}>
            Schedule
          </button>
          <button className={`tab ${view === "performance" ? "active" : ""}`} onClick={() => setView("performance")}>
            Performance
          </button>
        </nav>
        <div className={`signal ${signalState}`}>
          <span className="lamp" />
          {signalState}
        </div>
      </header>
      <main>
        {view === "pipeline" ? (
          <>
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
          </>
        ) : view === "carousel" ? (
          <CarouselPanel carousels={carousels} onChanged={loadCarousels} onGenerate={handleGenerateCarousel} onAuthor={handleAuthorCarousel} />
        ) : view === "schedule" ? (
          <SchedulePanel scripts={scripts} />
        ) : (
          <PerformancePanel />
        )}
      </main>
      <Toast toast={toast} onDismiss={() => setToast(null)} />
    </>
  );
}
