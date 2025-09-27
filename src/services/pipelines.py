import pendulum

from db.config import session_scope
from db.repositories.ad import AdRepository
from db.repositories.adset import AdSetRepository
from db.repositories.campaign import CampaignRepository
from db.repositories.insight import InsightRepository
from models import Campaign, AdSet, Ad, Insight
from services.loader import Loader, CampaignLoader, AdSetLoader, AdLoader, InsightLoader
from services.marketing import MetaMarketingAPIService


class MetaPipeline:
    def __init__(self, fb: MetaMarketingAPIService):
        self.fb = fb

    def upload(self, loader: Loader) -> tuple[list[Campaign], list[AdSet], list[Ad], list[Insight]]:
        campaigns = CampaignLoader(loader).load()
        adsets = AdSetLoader(loader).load()
        ads = AdLoader(loader).load()
        insights = InsightLoader(loader).load()

        for c in campaigns:
            c = self.fb.create_campaign(c)

            for insight in insights:
                if insight.campaign_id == c.campaign_id:
                    insight.campaign_id = c.fb_id

        for a in adsets:
            parent = next(c for c in campaigns if c.campaign_id == a.campaign_id)
            a.campaign_fb_id = parent.fb_id
            a = self.fb.create_adset(a)

            for insight in insights:
                if insight.adset_id == a.adset_id:
                    insight.adset_id = a.fb_id

        for ad in ads:
            parent = next(a for a in adsets if a.adset_id == ad.adset_id)
            ad.adset_fb_id = parent.fb_id
        #     self.fb.create_ad(ad) НЕ ПРАЦЮЄ ЧЕРЕЗ 1359188 ПОМИЛКУ НЕ ВКАЗАНИЙ МЕТОД ОПЛАТИ

        return campaigns, adsets, ads, insights

    def download(self):
        campaigns = sorted(self.fb.get_campaigns_list(), key=lambda c: c['id'])
        adsets = sorted(self.fb.get_adsets_list(), key=lambda a: a['id'])

        return campaigns, adsets

    def compare_sources_to_meta(self, campaigns_from_csv: list[Campaign], adsets_from_csv: list[AdSet]):
        campaigns_from_meta, adset_from_meta = self.download()

        for c_csv, c_meta in zip(campaigns_from_csv, campaigns_from_meta):
            c_csv.compare_to_downloaded_from_meta(c_meta)

        for a_csv, a_meta in zip(adsets_from_csv, adset_from_meta):
            a_csv.compare_to_downloaded_from_meta(a_meta)

    def delete_all_from_meta(self):
        self.fb.delete_all_campaigns()
        self.fb.delete_all_adsets()

    def upload_from_scratch(self, loader: Loader):
        self.delete_all_from_meta()
        campaigns, adsets, ads, insights = self.upload(loader)
        campaigns = sorted(campaigns, key=lambda c: c.fb_id)
        adsets = sorted(adsets, key=lambda a: a.fb_id)
        self.compare_sources_to_meta(campaigns, adsets)

        return campaigns, adsets, ads, insights

    def persist_all_to_db(
            self,
            campaigns:list[Campaign],
            adsets: list[AdSet],
            ads: list[Ad],
            insights: list[Insight],
    ):
        with session_scope() as s:
            n_c = CampaignRepository(s).upsert_many([campaign.to_db_row() for campaign in campaigns])
            n_as = AdSetRepository(s).upsert_many([adset.to_db_row() for adset in adsets])
            n_ad = AdRepository(s).upsert_many([ad.to_db_row() for ad in ads])
            n_fx = InsightRepository(s).upsert_many([insight.to_db_row() for insight in insights])
            print(f"Upserted → campaigns={n_c}, adsets={n_as}, ads={n_ad}, insights={n_fx}")

    def upsert_meta_data(self):
        campaigns, adsets = self.download()

        with session_scope() as s:
            n_c = CampaignRepository(s).upsert_many(
                [
                    {
                        'campaign_id': campaign['id'],
                        'campaign_name': campaign['name'],
                        'objective': campaign['objective'],
                        'status': campaign['status'],
                        'created_time': pendulum.parse(campaign['created_time'], strict=False).in_tz("UTC").naive(),
                    }
                    for campaign in campaigns
                ]
            )
            n_as = AdSetRepository(s).upsert_many(
                [
                    {
                        'adset_id': adset['id'],
                        'campaign_id': adset['campaign_id'],
                        'adset_name': adset['name'],
                        'status': adset['status'],
                        'bid_strategy': adset['bid_strategy'],
                        'daily_budget': adset['daily_budget'],
                        'start_time': pendulum.parse(adset['start_time'], strict=False).in_tz("UTC").naive(),
                    }
                    for adset in adsets
                ]
            )

            print(f"Upserted → campaigns={n_c}, adsets={n_as}")





