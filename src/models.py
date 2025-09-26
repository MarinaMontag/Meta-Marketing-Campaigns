from datetime import datetime

from pydantic import BaseModel

from settings import settings


class Campaign(BaseModel):
    campaign_id: str
    campaign_name: str
    objective: str
    status: str
    created_time: str
    fb_id: str | None = None

    def compare_to_downloaded_from_meta(self, c_meta: dict):
        print(f"Campaign {self.campaign_id} vs {c_meta['id']}")

        if self.fb_id and self.fb_id != c_meta['id']:
            print(f"Campaign {self.campaign_id} id not Meta campaign {c_meta['id']}")
            return

        if self.campaign_name == c_meta['name']:
            print(f"Name {self.campaign_name} == {c_meta['name']}")
        else:
            print(f"Name {self.campaign_name} != {c_meta['name']}")

        if self.objective == c_meta['objective']:
            print(f"Objective {self.objective} == {c_meta['objective']}")
        else:
            print(f"Objective {self.objective} != {c_meta['objective']}")

        if self.status == c_meta['status']:
            print(f"Status {self.status} == {c_meta['status']}")
        else:
            print(f"Status {self.status} != {c_meta['status']}")

        if datetime.fromisoformat(self.created_time) == datetime.fromisoformat(c_meta['created_time']):
            print(f"Created {self.created_time} == {c_meta['created_time']}")
        else:
            print(f"Created {self.created_time} != {c_meta['created_time']}")

        print('\n\n')

    def to_db_row(self) -> dict:
        return {
            "campaign_id": self.fb_id,
            "campaign_name": self.campaign_name,
            "objective": self.objective,
            "status": self.status,
            "created_time": self.created_time,
        }


class AdSet(BaseModel):
    adset_id: str
    campaign_id: str
    adset_name: str
    status: str
    bid_strategy: str
    daily_budget: int
    start_time: str
    fb_id: str | None = None
    campaign_fb_id: str | None = None

    def compare_to_downloaded_from_meta(self, a_meta: dict):
        print(f"Adset {self.adset_id} {self.fb_id} vs {a_meta['id']}")


        if self.fb_id and self.fb_id != a_meta['id']:
            print(f"Adset {self.campaign_id} id not Meta adset {a_meta['id']}")
            return

        if self.adset_name == a_meta['name']:
            print(f"Name {self.adset_name} == {a_meta['name']}")
        else:
            print(f"Name {self.adset_name} != {a_meta['name']}")

        if self.status == a_meta['status']:
            print(f"Status {self.status} == {a_meta['status']}")
        else:
            print(f"Status {self.status} != {a_meta['status']}")

        if self.bid_strategy == a_meta['bid_strategy']:
            print(f"bid_strategy {self.bid_strategy} == {a_meta['bid_strategy']}")
        else:
            print(f"bid_strategy {self.bid_strategy} != {a_meta['bid_strategy']}")

        if self.daily_budget == int(a_meta['daily_budget']):
            print(f"daily_budget {self.daily_budget} == {a_meta['daily_budget']}")
        else:
            print(f"daily_budget {self.daily_budget} != {a_meta['daily_budget']}")

        if datetime.fromisoformat(self.start_time) == datetime.fromisoformat(a_meta['start_time']):
            print(f"start_time {self.start_time} == {a_meta['start_time']}")
        else:
            print(f"start_time {self.start_time} != {a_meta['start_time']}")

        print('\n\n')

    def to_db_row(self) -> dict:
        return {
            'adset_id': self.fb_id,
            'campaign_id': self.campaign_fb_id,
            'adset_name': self.adset_name,
            'status': self.status,
            'bid_strategy': self.bid_strategy,
            'daily_budget': self.daily_budget,
            'start_time': self.start_time,
        }


class Ad(BaseModel):
    ad_id: str
    adset_id: str
    ad_name: str
    status: str
    creative_id: str
    created_time: str
    fb_id: str | None = None
    adset_fb_id: str | None = None

    def to_db_row(self) -> dict:
        return {
            'ad_id': self.ad_id,
            'adset_id': self.adset_fb_id,
            'ad_name': self.ad_name,
            'status': self.status,
            'creative_id': settings.META_CREATIVE_ID,
            'created_time': self.created_time,
        }


class Insight(BaseModel):
    date: str
    campaign_id: str
    adset_id: str
    ad_id: str
    impressions: int
    clicks: int
    spend: float
    conversions: int
    revenue: float

    def to_db_row(self) -> dict:
        return {
            'date': self.date,
            'campaign_id': self.campaign_id,
            'adset_id': self.adset_id,
            'ad_id': self.ad_id,
            'impressions': self.impressions,
            'clicks': self.clicks,
            'spend': self.spend,
            'conversions': self.conversions,
            'revenue': self.revenue,
        }