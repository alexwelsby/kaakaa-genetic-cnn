import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
export default defineConfig({
  base: "/static/react/",
  plugins: [react()],
  resolve: {
    mainFields: [],
  },
  alias: {
    "@": "/src",
    axios: path.resolve(__dirname, "node_modules/axios/index.js"),
  },
  optimizeDeps: {
    exclude: ["react-google-charts", "stream", "buffer"],
  },
  build: {
    outDir: path.resolve(__dirname, "../static/react"),
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules")) {
            // Split vendor code (libraries in node_modules) into a separate chunk
            return "vendor";
          }
        },
        assetFileNames: "[name]-[hash][extname]",
        chunkFileNames: "[name]-[hash].js",
        entryFileNames: "[name]-[hash].js",
      },
    },
    chunkSizeWarningLimit: 1000, // Adjust the warning limit (e.g., 1000 kBs)
  },
});
