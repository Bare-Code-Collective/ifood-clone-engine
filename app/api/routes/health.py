from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Health"])


@router.get("/")
def health_check() -> dict[str, str]:
    return {"status": "online", "service": "ifood-clone-engine"}
