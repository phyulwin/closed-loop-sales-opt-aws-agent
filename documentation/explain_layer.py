import boto3
import json
import logging
# from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource("dynamodb")
saleslog_table = dynamodb.Table("SalesAutomationProject_SalesLog")
explain_table = dynamodb.Table("SalesAutomationProject_Explanations")
cloudwatch = boto3.client("cloudwatch")

# You may wrap calls to Bedrock/Claude or Llama here
def generate_explanation(decision, context):
    bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

    prompt = f"""
    You are an experienced retail manager.
    Explain the following decision clearly and concisely in one sentence.

    Decision: {json.dumps(decision)}
    Context: {json.dumps(context)}

    Output only natural language explanation, e.g.
    "I lowered the price by 10% because sales dropped 20% last week."
    """

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # or "meta.llama3-70b-instruct-v1:0"
        body=json.dumps({
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.7
        }),
        contentType="application/json"
    )

    result = json.loads(response["body"].read())
    message = result["content"][0]["text"]
    return message.strip()

def save_explanation_log(product_id, timestamp, explanation, decision):
    item = {
        "product_id": product_id,
        "timestamp": timestamp,
        "decision": decision,
        "explanation": explanation
    }
    explain_table.put_item(Item=item)
    logger.info("Saved explanation log for %s", product_id)

def stream_to_cloudwatch(log_msg):
    try:
        cloudwatch.put_metric_data(
            Namespace="AgentExplainability",
            MetricData=[
                {
                    "MetricName": "ExplanationEvent",
                    "Value": 1,
                    "Unit": "Count",
                    "Dimensions": []
                }
            ]
        )
        # Also send text logs via CloudWatch Logs handled by Lambda by default
    except ClientError as e:
        logger.error("Failed to send to CloudWatch: %s", e)

def explain_decision(product_id, timestamp, decision, context):
    explanation = generate_explanation(decision, context)
    save_explanation_log(product_id, timestamp, explanation, decision)
    stream_to_cloudwatch(f"{product_id} @ {timestamp}: {explanation}")
    return explanation