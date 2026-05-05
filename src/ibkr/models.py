from typing import Any

from pydantic import AliasChoices, BaseModel, Field


class IBKRBaseModel(BaseModel):
    """Base model for all IBKR entities."""
    model_config = {"populate_by_name": True}

class Account(IBKRBaseModel):
    id: str = Field(alias="accountId")
    type: str
    currency: str
    summary: dict[str, Any] | None = None

class Position(IBKRBaseModel):
    conid: int
    symbol: str = Field(validation_alias=AliasChoices("contractDesc", "symbol"))
    size: float = Field(validation_alias=AliasChoices("position", "size"))
    avg_price: float = Field(validation_alias=AliasChoices("avgPrice", "avg_price"))
    mkt_price: float = Field(validation_alias=AliasChoices("mktPrice", "mkt_price"))
    mkt_value: float = Field(validation_alias=AliasChoices("mktValue", "mkt_value"))

class Contract(IBKRBaseModel):
    conid: int
    symbol: str
    asset_class: str = Field(alias="assetClass")
    exchange: str | None = None
    description: str | None = None

class MarketDataSnapshot(IBKRBaseModel):
    conid: int
    last: float | None = Field(None, alias="31")
    bid: float | None = Field(None, alias="84")
    ask: float | None = Field(None, alias="86")
    change: float | None = Field(None, alias="82")

class Order(IBKRBaseModel):
    id: str = Field(alias="orderId")
    conid: int
    side: str
    quantity: float = Field(validation_alias=AliasChoices("totalSize", "totalQuantity", "quantity"))
    remaining: float = Field(0.0, validation_alias=AliasChoices("remainingQuantity", "remaining"))
    order_type: str = Field(alias="orderType")
    lmt_price: float | None = Field(None, alias="lmtPrice")
    status: str
    symbol: str | None = Field(None, validation_alias=AliasChoices("ticker", "symbol"))
