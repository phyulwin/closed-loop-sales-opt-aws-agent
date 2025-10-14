import boto3
import random
import datetime
import logging
from decimal import Decimal
from agents.agent_core import choose_strategy
from explain_layer import explain_decision
from user_function import add_product, get_products, set_price, check_sales, simulate_sales, get_explanations

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
products_table = dynamodb.Table("SalesAutomationProject_Products")
saleslog_table = dynamodb.Table("SalesAutomationProject_SalesLog")

# ---------------- Lambda Handler ----------------
def lambda_handler(event, context):
    logger.info("Lambda triggered: %s", event)
    action = event.get("action")

    if action == "add_product":   return add_product(event)
    elif action == "get_products": return get_products(event)
    elif action == "set_price":    return set_price(event)
    elif action == "check_sales":  return check_sales(event)
    elif action == "simulate":     return simulate_sales(event)
    elif action == "agent_cycle":  return agent_cycle(event)
    elif action == "get_explanations": return get_explanations(event)
    else:
        return {"error": f"Unknown action {action}"}

# ---------------- AgentCore + Explainability ----------------
def agent_cycle(event):
    pid = event.get("product_id")
    if not pid: return {"error": "product_id required"}
    prod = products_table.get_item(Key={"product_id": pid}).get("Item")
    if not prod: return {"error": "Product not found"}
    if int(prod.get("inventory", 0)) <= 0:
        return {"status": "ok", "message": "Out of stock", "product_id": pid}

    strategies = ["discount", "bundle_buy2_get10off", "dynamic_pricing"]
    results = []
    for strat in strategies:
        sim = simulate_sales(event, promo_override=strat)
        price = float(sim.get("price", 0))
        sales = int(sim.get("sales", 0))
        revenue = round(price * sales, 2)
        profit = round(revenue * 0.3, 2)

        results.append({
            "strategy": strat,
            "sales": sales,
            "revenue": revenue,
            "profit": profit
        })

    best = max(results, key=lambda x: x["profit"])

    ts = datetime.datetime.utcnow().isoformat() + "Z"
    explanation = explain_decision(
        pid, ts, best["strategy"],
        {"sales_results": results, "inventory": prod.get("inventory")}
    )

    return {"status": "ok", "product_id": pid,
            "best_strategy": best, "explanation": explanation}