from db.repositories.base import BaseRepository
from db.schemas import DimAdSet


class AdSetRepository(BaseRepository):
    table = DimAdSet.__table__
    pk = ["adset_id"]
    updatable = [
        "campaign_id",
        "adset_name",
        "bid_strategy",
        "daily_budget",
        "status",
        "start_time",
    ]
