from app.schemas.domain import Location, OrderEvent, Restaurant, UserProfile


RESTAURANTS: list[Restaurant] = [
    Restaurant(
        id=1,
        name="Norte Sabor",
        cuisine="regional",
        avg_ticket_brl=32.0,
        rating=4.7,
        location=Location(lat=-3.1190, lon=-60.0217),
        is_open=True,
    ),
    Restaurant(
        id=2,
        name="Pizza Centro",
        cuisine="pizza",
        avg_ticket_brl=46.0,
        rating=4.5,
        location=Location(lat=-3.1010, lon=-60.0250),
        is_open=True,
    ),
    Restaurant(
        id=3,
        name="Fit Express",
        cuisine="saudavel",
        avg_ticket_brl=39.0,
        rating=4.2,
        location=Location(lat=-3.0865, lon=-60.0104),
        is_open=False,
    ),
    Restaurant(
        id=4,
        name="Burger da Praça",
        cuisine="hamburguer",
        avg_ticket_brl=41.0,
        rating=4.3,
        location=Location(lat=-3.1291, lon=-60.0082),
        is_open=True,
    ),
    Restaurant(
        id=5,
        name="Sushi Rio Negro",
        cuisine="japonesa",
        avg_ticket_brl=58.0,
        rating=4.6,
        location=Location(lat=-3.0958, lon=-60.0402),
        is_open=True,
    ),
    Restaurant(
        id=6,
        name="Massa Nobre",
        cuisine="italiana",
        avg_ticket_brl=52.0,
        rating=4.1,
        location=Location(lat=-3.1410, lon=-60.0290),
        is_open=True,
    ),
    Restaurant(
        id=7,
        name="Açaí da Ilha",
        cuisine="sobremesa",
        avg_ticket_brl=25.0,
        rating=4.4,
        location=Location(lat=-3.1214, lon=-60.0471),
        is_open=True,
    ),
    Restaurant(
        id=8,
        name="Grill 24h",
        cuisine="churrasco",
        avg_ticket_brl=48.0,
        rating=4.0,
        location=Location(lat=-3.0750, lon=-60.0312),
        is_open=True,
    ),
]

USERS: list[UserProfile] = [
    UserProfile(
        id=100,
        name="Victor",
        preferred_cuisines=["regional", "hamburguer", "pizza"],
        avg_spend_brl=42.0,
        location=Location(lat=-3.1072, lon=-60.0261),
    ),
    UserProfile(
        id=101,
        name="Ana",
        preferred_cuisines=["saudavel", "japonesa", "sobremesa"],
        avg_spend_brl=55.0,
        location=Location(lat=-3.0980, lon=-60.0410),
    ),
    UserProfile(
        id=102,
        name="Joao",
        preferred_cuisines=["pizza", "italiana", "churrasco"],
        avg_spend_brl=50.0,
        location=Location(lat=-3.1430, lon=-60.0205),
    ),
    UserProfile(
        id=103,
        name="Carla",
        preferred_cuisines=["regional", "hamburguer", "sobremesa"],
        avg_spend_brl=36.0,
        location=Location(lat=-3.1245, lon=-60.0460),
    ),
]

ORDER_EVENTS: list[OrderEvent] = [
    OrderEvent(user_id=100, restaurant_id=1, total_brl=35.0, hour=12),
    OrderEvent(user_id=100, restaurant_id=4, total_brl=43.0, hour=20),
    OrderEvent(user_id=100, restaurant_id=1, total_brl=33.0, hour=13),
    OrderEvent(user_id=100, restaurant_id=2, total_brl=49.0, hour=21),
    OrderEvent(user_id=101, restaurant_id=5, total_brl=62.0, hour=20),
    OrderEvent(user_id=101, restaurant_id=7, total_brl=24.0, hour=15),
    OrderEvent(user_id=102, restaurant_id=6, total_brl=54.0, hour=13),
    OrderEvent(user_id=102, restaurant_id=2, total_brl=47.0, hour=21),
    OrderEvent(user_id=103, restaurant_id=1, total_brl=34.0, hour=12),
    OrderEvent(user_id=103, restaurant_id=4, total_brl=44.0, hour=19),
]


def get_user(user_id: int) -> UserProfile | None:
    return next((user for user in USERS if user.id == user_id), None)
