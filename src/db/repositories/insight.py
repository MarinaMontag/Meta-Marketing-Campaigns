from db.repositories.base import BaseRepository
from db.schemas import FactInsightsDaily


class InsightRepository(BaseRepository):
    table = FactInsightsDaily.__table__
    pk = ["date", "ad_id"]
    updatable = [
        "campaign_id",
        "adset_id",
        "ad_id",
        "impressions",
        "clicks",
        "spend",
        "conversions",
        "revenue",
    ]