from db.repositories.base import BaseRepository
from db.schemas import DimCampaign


class CampaignRepository(BaseRepository):
    table = DimCampaign.__table__
    pk = ['campaign_id']
    updatable = [
        "campaign_name",
        "objective",
        "status",
    ]