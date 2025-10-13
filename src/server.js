import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

app.use(express.json());
app.use(express.static("src"));
app.use(express.static(path.join(__dirname, "dist"))); // serve React build

// TODO: Connect to DynamoDB
// import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
// const db = new DynamoDBClient({ region: "us-east-1" });

app.get("/api/products", (req, res) => {
  // TODO: Fetch product list from DynamoDB
  res.json([]); // placeholder
});

app.post("/api/products", (req, res) => {
  // TODO: Save updated products
  res.json({ message: "Saved" });
});

app.post("/api/start-agent", (req, res) => {
  // TODO: Trigger Lambda or run simulation logic
  res.json({ message: "Simulation started" });
});

app.get("/api/logs", (req, res) => {
  // TODO: Fetch logs or insights from DynamoDB
  res.json([]);
});

// app.listen(3000, () => console.log("Server running on http://localhost:3000"));