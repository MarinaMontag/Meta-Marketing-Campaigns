from db.repositories.base import BaseRepository
from db.schemas import DimAd


class AdRepository(BaseRepository):
    table = DimAd.__table__
    pk = ["ad_id"]
    updatable = [
        "adset_id",
        "ad_name",
        "creative_id",
        "status",
    ]