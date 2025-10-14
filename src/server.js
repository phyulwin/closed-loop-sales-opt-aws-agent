import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { DynamoDBClient, PutItemCommand, ScanCommand } from "@aws-sdk/client-dynamodb";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());

// Connect to DynamoDB
const db = new DynamoDBClient({ region: "us-east-1" });
const TABLE_NAME = "ShopInventory"; // make sure this matches your DynamoDB table name

// Get all products
app.get("/api/products", async (req, res) => {
  try {
    const result = await db.send(new ScanCommand({ TableName: TABLE_NAME }));
    const items = result.Items.map(i => ({
      product_id: i.product_id.S,
      name: i.name.S,
      price: Number(i.price.N),
      stock: Number(i.stock.N)
    }));
    res.json(items);
  } catch (err) {
    console.error("Error fetching products:", err);
    res.status(500).json({ error: "Failed to fetch products" });
  }
});

// Add or update product
app.post("/api/products", async (req, res) => {
  const { product_id, name, price, stock } = req.body;
  if (!product_id || !name || price == null || stock == null)
    return res.status(400).json({ error: "Missing fields" });

  try {
    await db.send(
      new PutItemCommand({
        TableName: TABLE_NAME,
        Item: {
          product_id: { S: product_id },
          name: { S: name },
          price: { N: price.toString() },
          stock: { N: stock.toString() }
        }
      })
    );
    res.json({ message: "Product saved" });
  } catch (err) {
    console.error("Error saving product:", err);
    res.status(500).json({ error: "Failed to save product" });
  }
});

// Optional: simulate agent start
app.post("/api/start-agent", (req, res) => {
  res.json({ message: "Agent started (mock)" });
});

// Serve frontend
app.use(express.static("src"));
app.use(express.static(path.join(__dirname, "dist")));

app.listen(3000, () => console.log("Server running on http://localhost:3000"));