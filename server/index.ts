import * as express from "express";
import * as cors from "cors";
import "dotenv/config";

export function createServer() {
  const app = express();

  app.use(cors());
  app.use(express.json());

  app.get("/api/ping", (req, res) => {
    res.json({ message: "pong" });
  });

  return app;
}

const port = process.env.PORT || 3000;

createServer().listen(port, () => {
  console.log(`🚀 Server running on http://localhost:${port}`);
});