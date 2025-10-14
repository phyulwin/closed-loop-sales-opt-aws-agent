import boto3, random, datetime, logging
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from explain_layer import explain_decision   # Week 3 layer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
cloudwatch = boto3.client("cloudwatch")

products_table = dynamodb.Table("SalesAutomationProject_Products")
saleslog_table = dynamodb.Table("SalesAutomationProject_SalesLog")
explain_table = dynamodb.Table("SalesAutomationProject_Explanations")

# ---------------- Product Management ----------------
def add_product(event):
    product_id = event.get("product_id")
    name = event.get("name")
    price = event.get("price")
    stock = event.get("stock", 0)
    desc = event.get("description", "")
    if not (product_id and name and price is not None):
        return {"error": "product_id, name, and price required"}

    products_table.put_item(Item={
        "product_id": product_id,
        "name": name,
        "price": Decimal(str(price)),
        "inventory": int(stock),
        "description": desc,
        "baseline_sales": 10,
        "price_sensitivity": -0.3
    })
    return {"status": "ok", "message": f"{name} added"}

def get_products(event):
    resp = products_table.scan()
    return {"products": resp.get("Items", [])}

def set_price(event):
    pid, newp = event.get("product_id"), event.get("new_price")
    if not pid or newp is None:
        return {"error": "product_id and new_price required"}
    products_table.update_item(
        Key={"product_id": pid},
        UpdateExpression="SET price=:p",
        ExpressionAttributeValues={":p": Decimal(str(newp))}
    )
    return {"status": "ok", "product_id": pid, "new_price": newp}

# ---------------- Sales + Simulation ----------------
def check_sales(event):
    pid = event.get("product_id")
    if not pid: return {"error": "product_id required"}
    resp = saleslog_table.query(
        KeyConditionExpression=Key("product_id").eq(pid),
        ScanIndexForward=False, Limit=10
    )
    return {"product_id": pid, "sales": resp.get("Items", [])}

def simulate_sales(event, promo_override=None):
    pid = event.get("product_id")
    if not pid: return {"error": "product_id required"}
    prod = products_table.get_item(Key={"product_id": pid}).get("Item")
    if not prod: return {"error": "Product not found"}

    price = Decimal(prod.get("price", 20))
    base = int(prod.get("baseline_sales", 10))
    sens = Decimal(prod.get("price_sensitivity", -0.3))
    inv  = int(prod.get("inventory", 0))

    promo = promo_override or event.get("promo", "none")
    sales = max(0, min(int(base + (Decimal(prod["price"]) - price) * sens * base), inv))
    if promo == "discount": sales = int(sales * 1.1)
    elif promo == "bundle_buy2_get10off": sales = int(sales * 1.15)
    elif promo == "dynamic_pricing": sales = int(sales * (0.8 + random.random() * 0.4))

    new_inv = inv - sales
    products_table.update_item(Key={"product_id": pid},
        UpdateExpression="SET inventory=:i",
        ExpressionAttributeValues={":i": new_inv})

    ts = datetime.datetime.utcnow().isoformat() + "Z"
    saleslog_table.put_item(Item={
        "product_id": pid, "timestamp": ts,
        "price": price, "promo": promo, "sales": sales
    })

    try:
        cloudwatch.put_metric_data(
            Namespace="EcommerceSimulation",
            MetricData=[{
                "MetricName": "Sales", "Dimensions":[{"Name":"Product","Value":pid}],
                "Value": sales, "Unit": "Count"
            }]
        )
    except Exception as e:
        logger.error("CloudWatch error: %s", e)

    return {
        "status": "ok",
        "product_id": product_id,
        "timestamp": timestamp,
        "price": price,
        "promo": promo,
        "sales": sales,
        "inventory": new_inventory
    }

# ---------------- Explainability Log Retrieval ----------------
def get_explanations(event):
    pid = event.get("product_id")
    if not pid: return {"error": "product_id required"}
    resp = explain_table.query(
        KeyConditionExpression=Key("product_id").eq(pid),
        ScanIndexForward=False, Limit=10
    )
    return {"product_id": pid, "explanations": resp.get("Items", [])}
