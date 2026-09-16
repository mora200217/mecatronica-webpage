import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En Docker el backend es otro contenedor; fuera, el runserver local.
const target = process.env.VITE_API_PROXY || "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    watch: { usePolling: !!process.env.VITE_POLL },
    proxy: {
      "/api": target,
      "/go": target,
      "/admin": target,
      "/static": target,
      "/uploads": target,
    },
  },
});
