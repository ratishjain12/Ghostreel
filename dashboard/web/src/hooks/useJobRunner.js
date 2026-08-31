import { useState, useCallback } from "react";
import { api } from "../api";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export function useJobRunner() {
  const [lines, setLines] = useState([]);
  const [status, setStatus] = useState("idle");

  const run = useCallback(async (starter) => {
    setLines([]);
    setStatus("running");
    try {
      const { job_id } = await starter();
      let since = 0;
      for (;;) {
        const data = await api.jobStatus(job_id, since);
        if (data.lines.length) setLines((prev) => [...prev, ...data.lines]);
        since = data.next;
        if (data.status !== "running") {
          setStatus(data.status);
          return data;
        }
        await sleep(700);
      }
    } catch (err) {
      setStatus("error");
      setLines((prev) => [...prev, `[dashboard] ${err.message}`]);
      return null;
    }
  }, []);

  return { lines, status, run };
}
