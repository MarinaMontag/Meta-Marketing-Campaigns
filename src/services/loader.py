from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, Mapping, Any, ClassVar

import pandas

from models import Campaign, AdSet, Ad, Insight


class Loader(ABC):
    file_format: str

    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)

    @abstractmethod
    def load(self, path: Path) -> Iterable[Mapping[str, Any]]:
        ...


class CSVLoader(Loader):
    file_format = "csv"

    def load(self, path: Path) ->  Iterable[Mapping[str, Any]]:
        return pandas.read_csv(path).to_dict(orient='records')


class EntityLoader:
    FILE_STEM: ClassVar[str] = ""

    def __init__(self, loader: Loader) -> None:
        self.loader = loader

    @property
    def file_path(self) -> Path:
        return self.loader.base_dir / f"{self.FILE_STEM}.{self.loader.file_format}"

    def load(self) -> list:
        ...


class CampaignLoader(EntityLoader):
    FILE_STEM = 'campaigns'

    def load(self) -> list[Campaign]:
        campaigns = self.loader.load(self.file_path)

        return (
            [
                Campaign(
                    campaign_id=c['campaign_id'],
                    campaign_name=c['campaign_name'],
                    objective=c['objective'],
                    status=c['status'],
                    created_time=c['created_time'],
                ) for c in campaigns
            ]
        )


class AdSetLoader(EntityLoader):
    FILE_STEM = 'adsets'

    def load(self) -> list[AdSet]:
        adsets = self.loader.load(self.file_path)

        return (
            [
                AdSet(
                    adset_id=a['adset_id'],
                    campaign_id=a['campaign_id'],
                    adset_name=a['adset_name'],
                    status=a['status'],
                    bid_strategy=a['bid_strategy'],
                    daily_budget=a['daily_budget'],
                    start_time=a['start_time'],
                ) for a in adsets
            ]
        )


class AdLoader(EntityLoader):
    FILE_STEM = 'ads'

    def load(self) -> list[Ad]:
        ads = self.loader.load(self.file_path)

        return (
            [
                Ad(
                    ad_id=ad['ad_id'],
                    adset_id=ad['adset_id'],
                    ad_name=ad['ad_name'],
                    status=ad['status'],
                    creative_id=ad['creative_id'],
                    created_time=ad['created_time'],
                ) for ad in ads
            ]
        )


class InsightLoader(EntityLoader):
    FILE_STEM = 'insights'

    def load(self) -> list[Insight]:
        insights = self.loader.load(self.file_path)

        return (
            [
                Insight(
                    date=i['date'],
                    campaign_id=i['campaign_id'],
                    adset_id=i['adset_id'],
                    ad_id=i['ad_id'],
                    impressions=i['impressions'],
                    clicks=i['clicks'],
                    spend=i['spend'],
                    conversions=i['conversions'],
                    revenue=i['revenue'],
                ) for i in insights
            ]
        )
