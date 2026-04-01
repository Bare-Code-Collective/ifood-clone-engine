from app.services.data_store import get_user
from app.services.recommender import rank_recommendations_for_user


def test_rank_recommendations_returns_sorted_scores() -> None:
    user = get_user(100)
    assert user is not None

    recs = rank_recommendations_for_user(user=user, top_n=5)
    assert len(recs) > 0

    scores = [item.score_final for item in recs]
    assert scores == sorted(scores, reverse=True)


def test_recommendations_are_viable_by_design() -> None:
    user = get_user(100)
    assert user is not None

    recs = rank_recommendations_for_user(user=user, top_n=5)
    assert all(item.distance_km <= 8.0 for item in recs)
    assert all(item.eta_min <= 45 for item in recs)
    assert all(item.delivery_fee_brl <= 12.0 for item in recs)
