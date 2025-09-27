from sqlalchemy import BigInteger, String, DateTime, Index, MetaData, ForeignKey, PrimaryKeyConstraint, DECIMAL, Column
from sqlalchemy.orm import relationship, declarative_base

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

Base = declarative_base(metadata=MetaData(naming_convention=NAMING_CONVENTION))


class DimCampaign(Base):
    __tablename__ = "dim_campaign"

    campaign_id = Column(BigInteger, primary_key=True)
    campaign_name = Column(String(255), nullable=False)
    objective = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    created_time = Column(DateTime, nullable=False)

    adsets = relationship('DimAdSet', back_populates="campaign")


class DimAdSet(Base):
    __tablename__ = "dim_adset"

    adset_id = Column(BigInteger, primary_key=True)
    campaign_id = Column(
        BigInteger,
        ForeignKey("dim_campaign.campaign_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    adset_name = Column(String(255), nullable=False)
    bid_strategy = Column(String(64), nullable=False)
    daily_budget = Column(BigInteger)
    status = Column(String(32), nullable=False)
    start_time = Column(DateTime, nullable=False)

    campaign = relationship('DimCampaign', back_populates="adsets")
    ads = relationship('DimAd', back_populates="adset")


class DimAd(Base):
    __tablename__ = "dim_ad"

    ad_id = Column(String(32), primary_key=True)
    adset_id = Column(
        BigInteger,
        ForeignKey("dim_adset.adset_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    ad_name = Column(String(255), nullable=False)
    creative_id = Column(BigInteger, nullable=False)
    status = Column(String(32), nullable=False)
    created_time = Column(DateTime, nullable=False)

    adset = relationship('DimAdSet', back_populates="ads")


class FactInsightsDaily(Base):
    __tablename__ = "fact_insights_daily"

    date = Column(DateTime, nullable=False)
    campaign_id = Column(
        BigInteger,
        ForeignKey("dim_campaign.campaign_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    adset_id = Column(
        BigInteger,
        ForeignKey("dim_adset.adset_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    ad_id = Column(
        String(32),
        ForeignKey("dim_ad.ad_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    impressions = Column(BigInteger, default=0)
    clicks = Column(BigInteger, default=0)
    spend = Column(DECIMAL(18, 6), default=0)
    conversions = Column(BigInteger, default=0)
    revenue = Column(DECIMAL(18, 6), default=0)

    __table_args__ = (
        PrimaryKeyConstraint("date", "ad_id", name="pk_fact_insights_daily"),
        Index("idx_fact_campaign_date", "campaign_id", "date"),
        Index("idx_fact_adset_date", "adset_id", "date"),
    )
