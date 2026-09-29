import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../static",
    emptyOutDir: true,
  },
  server: {
    // true (not just localhost) so the dashboard is reachable from a phone on the
    // same trusted home Wi-Fi — prints the LAN URL to the terminal on start.
    host: true,
    proxy: {
      "/api": "http://127.0.0.1:8787",
      "/media": "http://127.0.0.1:8787",
      "/carousel-media": "http://127.0.0.1:8787",
      "/growth-data": "http://127.0.0.1:8787",
    },
  },
});
