from fastapi import APIRouter

from app.services.data_store import ORDER_EVENTS

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/events/summary")
def events_summary() -> dict[str, float]:
    total_orders = len(ORDER_EVENTS)
    total_revenue = sum(event.total_brl for event in ORDER_EVENTS)
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
    return {
        "total_orders": total_orders,
        "total_revenue_brl": round(total_revenue, 2),
        "avg_order_value_brl": round(avg_order_value, 2),
    }
