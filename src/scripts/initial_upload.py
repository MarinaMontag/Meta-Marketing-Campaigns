from services.loader import CSVLoader
from services.marketing import MetaMarketingAPIService
from services.pipelines import MetaPipeline
from settings import settings


pipeline = MetaPipeline(MetaMarketingAPIService(settings.META_ACCESS_TOKEN, settings.META_AD_ACCOUNT_ID))
campaigns, adsets, ads, insights = pipeline.upload_from_scratch(CSVLoader(settings.CSV_DIR))
pipeline.persist_all_to_db(campaigns, adsets, ads, insights)
