# Documenting Setup Steps (Week 1)

## **1. Start With Context**

* Add a short intro:

  > *“This section describes how to set up the fake e-commerce shop and demand simulator. By the end, you’ll have a DynamoDB-backed store with a Lambda that simulates daily sales.”*
* Clarify what the reader is about to build and why it matters.

This project shows how AI can autonomously test, adapt, and optimize pricing strategies without constant human oversight. It helps companies by boosting sales through data-driven experiments, providing clear reasoning for decisions, and scaling efficiently. However, results depend heavily on data quality and realistic demand modeling.
---

## **2. List Prerequisites**

Clearly state what’s needed before setup:

* AWS account with access to **DynamoDB, Lambda, CloudWatch**.
* IAM permissions: create/read/write tables, deploy Lambda, manage logs.
* Tools installed locally:

  * AWS CLI (configured with credentials)
  * Node.js or Python (depending on Lambda runtime)
  * Git (to clone repo)

---

## **3. Step-By-Step Instructions**

Break it down into **clear, numbered steps** with code blocks and expected outputs.

**Example structure:**

1. **Clone the repo**

   ```bash
   git clone https://github.com/phyulwin/closed-loop-sales-opt-aws-agent.git
   cd hackathon-agent
   ```

2. **Create DynamoDB tables**

   ```bash
   aws dynamodb create-table \
     --table-name Products \
     --attribute-definitions AttributeName=ProductID,AttributeType=S \
     --key-schema AttributeName=ProductID,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST
   ```

   * Products table holds: `ProductID`, `Price`, `Inventory`.
   * SalesLogs table holds: `Timestamp`, `Price`, `Sales`.

3. **Deploy Lambda demand simulator**

   * Show the exact command (AWS SAM / CDK / zip + upload).
   * Note runtime (e.g., Python 3.9).
   * Include environment variable configuration (e.g., table names).

4. **Grant IAM permissions**

   * Attach policy allowing Lambda to read/write DynamoDB and write to CloudWatch.
   * Example JSON snippet.

5. **Test baseline**

   ```bash
   aws lambda invoke \
     --function-name DemandSimulator \
     --payload '{"price":28}' response.json
   cat response.json
   ```

   Expected output: \~10 sales/day at \$28.

---

## **4. Verify Setup**

* Show how to check DynamoDB for inserted sales logs.
* Show how to view CloudWatch logs to confirm Lambda execution.
* Provide example log output.

---

## **5. Troubleshooting Tips**

Add a small section for common issues:

* *PermissionDenied*: check IAM role.
* *Lambda timeout*: increase function timeout to 30s.
* *DynamoDB table not found*: verify table names match environment variables.

---

## **6. Close With Deliverable**

Conclude with a confirmation sentence:

> *“At this stage, your fake shop is live: DynamoDB stores sales, the Lambda simulator reacts to price changes, and logs appear in CloudWatch.”*