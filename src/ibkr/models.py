from typing import Any

from pydantic import AliasChoices, BaseModel, Field


class IBKRBaseModel(BaseModel):
    """Base model for all IBKR entities."""
    model_config = {"populate_by_name": True}

class Account(IBKRBaseModel):
    id: str | None = Field(None, alias="accountId")
    type: str | None = None
    currency: str | None = None
    summary: dict[str, Any] | None = None

class Position(IBKRBaseModel):
    conid: int | None = None
    symbol: str | None = Field(
        None, validation_alias=AliasChoices("contractDesc", "symbol")
    )
    size: float = Field(0.0, validation_alias=AliasChoices("position", "size"))
    avg_price: float = Field(
        0.0, validation_alias=AliasChoices("avgPrice", "avg_price")
    )
    mkt_price: float = Field(
        0.0, validation_alias=AliasChoices("mktPrice", "mkt_price")
    )
    mkt_value: float = Field(
        0.0, validation_alias=AliasChoices("mktValue", "mkt_value")
    )

class Contract(IBKRBaseModel):
    conid: int | None = None
    symbol: str | None = None
    asset_class: str | None = Field(None, alias="assetClass")
    exchange: str | None = None
    description: str | None = None

class MarketDataSnapshot(IBKRBaseModel):
    conid: int | None = None
    last: float | None = Field(None, alias="31")
    bid: float | None = Field(None, alias="84")
    ask: float | None = Field(None, alias="86")
    change: float | None = Field(None, alias="82")

class Order(IBKRBaseModel):
    id: str | None = Field(None, alias="orderId")
    conid: int | None = None
    side: str | None = None
    quantity: float = Field(
        0.0,
        validation_alias=AliasChoices("totalSize", "totalQuantity", "quantity")
    )
    remaining: float = Field(
        0.0,
        validation_alias=AliasChoices("remainingQuantity", "remaining")
    )
    order_type: str | None = Field(None, alias="orderType")
    lmt_price: float | None = Field(None, alias="lmtPrice")
    status: str | None = None
    symbol: str | None = Field(None, validation_alias=AliasChoices("ticker", "symbol"))
