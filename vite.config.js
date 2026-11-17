import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function serveImagesPlugin() {
  return {
    name: 'serve-images-plugin',
    configureServer(server) {
      server.middlewares.use('/images', (req, res, next) => {
        try {
          const rawUrl = req.url || '';
          const decoded = decodeURIComponent(rawUrl.split('?')[0]);
          const cleanPath = decoded.replace(/^\//, '');
          const filePath = path.join(__dirname, 'images', cleanPath);

          if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
            const ext = path.extname(filePath).toLowerCase();
            const mimeTypes = {
              '.jpeg': 'image/jpeg',
              '.jpg': 'image/jpeg',
              '.png': 'image/png',
              '.svg': 'image/svg+xml',
              '.webp': 'image/webp',
              '.gif': 'image/gif',
            };
            res.setHeader('Content-Type', mimeTypes[ext] || 'application/octet-stream');
            res.setHeader('Cache-Control', 'public, max-age=3600');
            fs.createReadStream(filePath).pipe(res);
            return;
          }
        } catch (err) {
          console.error('Error serving image:', err);
        }
        next();
      });
    },
    closeBundle() {
      // Copy images folder into dist/images for production builds
      const srcDir = path.resolve(__dirname, 'images');
      const destDir = path.resolve(__dirname, 'dist', 'images');
      if (fs.existsSync(srcDir)) {
        fs.mkdirSync(destDir, { recursive: true });
        fs.cpSync(srcDir, destDir, { recursive: true });
        console.log('✅ Copied images folder to dist/images for production build.');
      }
    }
  };
}

export default defineConfig({
  plugins: [react(), serveImagesPlugin()],
  server: {
    port: 3000,
    open: false,
    host: true,
  },
  build: {
    outDir: 'dist',
    assetsInlineLimit: 4096,
  }
});
