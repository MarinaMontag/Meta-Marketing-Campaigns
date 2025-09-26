import time

import requests

from models import Campaign, AdSet, Ad
from settings import settings


class MetaMarketingAPIError(RuntimeError):
    pass


class MetaMarketingAPIService:
    def __init__(self, access_token, ad_account_id):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = f'{settings.META_GRAPH_BASE}/{settings.META_GRAPH_VERSION}'
        self.timeout = settings.REQUEST_TIMEOUT_SEC

    def _post(self, path: str, data: dict) -> dict:
        try:
            response = requests.post(
                f'{self.base_url}/{path}',
                json={**data, 'access_token': self.access_token},
                timeout=self.timeout,
            )
            response.raise_for_status()
            time.sleep(5)

            return response.json()
        except requests.RequestException as e:
            raise MetaMarketingAPIError(f'POST {path} failed: {e}') from e

    def _get(self, path: str, fields: str) -> dict:
        try:
            response = requests.get(
                f'{self.base_url}/{path}',
                params={
                    'fields': fields,
                    'access_token': self.access_token,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            time.sleep(5)

            return response.json()
        except requests.RequestException as e:
            raise MetaMarketingAPIError(f'GET {path} failed: {e}') from e

    def _delete(self, id: str) -> dict:
        try:
            response = requests.delete(
                f'{self.base_url}/{id}',
                params={'access_token': self.access_token},
                timeout=self.timeout,
            )
            response.raise_for_status()
            time.sleep(5)

            return response.json()
        except requests.RequestException as e:
            raise MetaMarketingAPIError(f'DELETE {id} failed: {e}') from e

    def create_campaign(self, c: Campaign) -> Campaign:
        response = self._post(
            f'{self.ad_account_id}/campaigns',
            {
                'name': c.campaign_name,
                'objective': c.objective,
                'status': c.status,
                'created_time': c.created_time,
                'special_ad_categories': ['NONE'],
            },
        )
        c.fb_id = response['id']

        return c

    def create_adset(self, a: AdSet) -> AdSet:
        response = self._post(
            f'{self.ad_account_id}/adsets',
            {
                'name': a.adset_name,
                'campaign_id': a.campaign_fb_id,
                'status': a.status,
                'bid_strategy': a.bid_strategy,
                'bid_amount': 1,
                'daily_budget': a.daily_budget,
                'start_time': a.start_time,
                'end_time': '2026-01-10T00:00:00.000',
                'billing_event': 'IMPRESSIONS',
                'optimization_goal': 'LINK_CLICKS',
                'targeting': {'geo_locations': {'countries': ['US']}},
            },
        )
        a.fb_id = response['id']

        return a

    def create_ad(self, ad: Ad) -> Ad:
        response = self._post(
            f'{self.ad_account_id}/ads',
            {
                'name': ad.ad_name,
                'adset_id': ad.adset_fb_id,
                'status': ad.status,
                'creative': {'creative_id': settings.META_CREATIVE_ID},
                'created_time': ad.created_time,
            },
        )
        ad.fb_id = response['id']

        return ad

    def get_campaigns_list(self) -> list[dict]:
        response = self._get(
            f'{self.ad_account_id}/campaigns',
            'id,name,objective,status,created_time',
        )

        return response['data']

    def get_adsets_list(self) -> list[dict]:
        response = self._get(
            f'{self.ad_account_id}/adsets',
            'id,name,campaign_id,status,bid_strategy,daily_budget,start_time',
        )

        return response['data']

    def delete_all_campaigns(self) -> None:
        campaigns = self.get_campaigns_list()

        for campaign in campaigns:
            self._delete(campaign['id'])

    def delete_all_adsets(self) -> None:
        adsets = self.get_adsets_list()

        for adset in adsets:
            self._delete(adset['id'])
