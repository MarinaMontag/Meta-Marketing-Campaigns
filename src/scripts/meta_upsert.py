from services.loader import CSVLoader
from services.marketing import MetaMarketingAPIService
from services.pipelines import MetaPipeline
from settings import settings

pipeline = MetaPipeline(
        CSVLoader(settings.CSV_DIR),
        MetaMarketingAPIService(settings.META_ACCESS_TOKEN, settings.META_AD_ACCOUNT_ID),
    )
pipeline.upsert_meta_data()