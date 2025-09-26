from datetime import datetime
from typing import List, Optional

from sqlalchemy import BigInteger, String, DateTime, Index, MetaData, ForeignKey, PrimaryKeyConstraint, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata_obj = MetaData(naming_convention=NAMING_CONVENTION)

class Base(DeclarativeBase):
    metadata = metadata_obj

class DimCampaign(Base):
    __tablename__ = "dim_campaign"
    campaign_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    campaign_name: Mapped[str] = mapped_column(String(255), nullable=False)
    objective: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    adsets: Mapped[List['DimAdSet']] = relationship(back_populates="campaign")


class DimAdSet(Base):
    __tablename__ = "dim_adset"
    adset_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("dim_campaign.campaign_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    adset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bid_strategy: Mapped[str] = mapped_column(String(64), nullable=False)
    daily_budget: Mapped[Optional[int]] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    campaign: Mapped["DimCampaign"] = relationship(back_populates="adsets")
    ads: Mapped[List["DimAd"]] = relationship(back_populates="adset")


class DimAd(Base):
    __tablename__ = "dim_ad"
    ad_id: Mapped[int] = mapped_column(String(32), primary_key=True)
    adset_id: Mapped[int] = mapped_column(ForeignKey("dim_adset.adset_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    ad_name: Mapped[str] = mapped_column(String(255), nullable=False)
    creative_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    adset: Mapped["DimAdSet"] = relationship(back_populates="ads")


class FactInsightsDaily(Base):
    __tablename__ = "fact_insights_daily"
    # PK (date, ad_id)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("dim_campaign.campaign_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    adset_id: Mapped[int] = mapped_column(ForeignKey("dim_adset.adset_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    ad_id: Mapped[int] = mapped_column(ForeignKey("dim_ad.ad_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=True)

    impressions: Mapped[int] = mapped_column(BigInteger, default=0)
    clicks: Mapped[int] = mapped_column(BigInteger, default=0)
    spend: Mapped[float] = mapped_column(DECIMAL(18, 6), default=0)
    conversions: Mapped[int] = mapped_column(BigInteger, default=0)
    revenue: Mapped[float] = mapped_column(DECIMAL(18, 6), default=0)

    __table_args__ = (
        PrimaryKeyConstraint("date", "ad_id", name="pk_fact_insights_daily"),
        Index("idx_fact_campaign_date", "campaign_id", "date"),
        Index("idx_fact_adset_date", "adset_id", "date"),
    )
