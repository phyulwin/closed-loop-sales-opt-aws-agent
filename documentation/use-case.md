### **Shopkeeper (Human actions)**

These are the things the **frontend** (HTML/JS) lets the shopkeeper do:

1. **Add new products**

   * Inputs: product name, base price, category, description.
   * Action: sends data to API Gateway → Lambda → DynamoDB stores it.

2. **View current products**

   * Sees product list with current price, sales, and offers (fetched from DynamoDB).

3. **Run the optimization agent**

   * Clicks “Run Agent” → triggers API Gateway → Lambda executes the AI agent loop.

4. **View agent’s recommendations**

   * Reads price changes, discounts, and reasoning text pulled from DynamoDB or CloudWatch logs.

5. **Approve or reject agent suggestions (optional)**

   * In human-in-the-loop setups, can choose whether to apply the agent’s changes.

---

### **AI Agent (Autonomous actions)**

These are what your **Python Bedrock agent** can do automatically:

1. **Read product and sales data from DynamoDB**

   * Pulls current price, sales volume, and trends.

2. **Simulate or analyze demand**

   * Uses your simulator or real data to estimate performance for each price point.

3. **Make strategic decisions**

   * Suggests or applies:

     * Dynamic price changes
     * Discount offers
     * Bundle deals
     * Volume discounts

4. **Write updates to DynamoDB**

   * Saves new prices, promotions, and reasoning logs.

5. **Log reasoning to CloudWatch**

   * Sends clear explanations like “Reduced price by 10% due to low sales.”

6. **Communicate results via API Gateway**

   * Sends structured JSON for the frontend to display.

7. **Optionally self-improve**

   * Tracks which strategy worked best and updates its logic.