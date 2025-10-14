import boto3, json, datetime
from strands import Agent, tool
from bedrock_agentcore import BedrockAgentCoreApp
import traceback

# ---------- Setup ----------
app = BedrockAgentCoreApp()
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# ---------- Tools ----------
@tool
def calculator(a: float, b: float) -> float:
    return a / b

@tool
def current_time():
    return str(datetime.datetime.now())

@tool
def letter_counter(word: str, letter: str) -> int:
    return word.lower().count(letter.lower())

@tool
def demand_simulator(price: float) -> float:
    """Fake demand curve: lower price = higher sales."""
    baseline_sales = 10
    elasticity = 0.5
    simulated_sales = baseline_sales * (28 / price) ** elasticity
    return round(simulated_sales, 2)

# ---------- Agent Setup ----------
agent = Agent(tools=[calculator, current_time, letter_counter, demand_simulator])

# ---------- Helper ----------
def ask_bedrock(prompt: str) -> str:
    """Send message to Claude 3.5 Sonnet and return text only."""
    body = {
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "max_tokens": 1000,
        "anthropic_version": "bedrock-2023-05-31"
    }
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=json.dumps(body)
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

# ---------- Core Logic ----------
@app.entrypoint
def invoke(payload):
    """Run a full optimization cycle."""
    price = payload.get("price", 28.0)
    sales = demand_simulator(price)

    prompt = (
        f"Current price: ${price:.2f}, daily sales: {sales} units.\n"
        "Suggest a new price or bundling strategy to improve profit."
    )
    suggestion = ask_bedrock(prompt)

    return {
        "timestamp": current_time(),
        "input_price": price,
        "simulated_sales": sales,
        "agent_suggestion": suggestion
    }

# ---------- Run ----------
if __name__ == "__main__":
    try:
        # print("Running Closed-Loop Sales Optimization Agent...")
        # test_payload = {"price": 28.0}
        # result = invoke(test_payload)
        # print(json.dumps(result, indent=2))
        print("Agent running successfully.")
        result = invoke({"price": 28.0})
        print("\n--- Summary ---")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Input price: ${result['input_price']}")
        print(f"Simulated sales: {result['simulated_sales']} units")
        # write agent suggestion output to a file
        with open("my_agent/agent_output.txt", "w", encoding="utf-8") as f:
            f.write(result["agent_suggestion"])
        print("Full response saved to agent_output.txt")

    except Exception as e:
        print("Error running agent:", e)
        traceback.print_exc()

#python -u my_agent/agent.py