from ibkr.models import Account, Contract, MarketDataSnapshot, Order, Position


def test_account_model():
    data = {
        "accountId": "U12345",
        "type": "INDIVIDUAL",
        "currency": "USD",
        "summary": {"NetLiquidation": 1000.0}
    }
    acc = Account(**data)
    assert acc.id == "U12345"
    assert acc.summary["NetLiquidation"] == 1000.0

def test_position_model():
    data = {
        "conid": 265598,
        "symbol": "AAPL",
        "position": 100,
        "avgPrice": 150.0,
        "mktPrice": 155.0,
        "mktValue": 15500.0
    }
    pos = Position(**data)
    assert pos.conid == 265598
    assert pos.size == 100
    assert pos.avg_price == 150.0

def test_contract_model():
    data = {
        "conid": 265598,
        "symbol": "AAPL",
        "assetClass": "STK",
        "exchange": "NASDAQ"
    }
    con = Contract(**data)
    assert con.conid == 265598
    assert con.asset_class == "STK"

def test_market_data_model():
    data = {
        "conid": 265598,
        "31": 155.0,
        "84": 154.5,
        "86": 155.5,
        "82": 0.5
    }
    md = MarketDataSnapshot(**data)
    assert md.conid == 265598
    assert md.last == 155.0

def test_order_model():
    data = {
        "orderId": "O1001",
        "conid": 265598,
        "side": "BUY",
        "quantity": 10,
        "orderType": "LMT",
        "lmtPrice": 150.0,
        "status": "Submitted"
    }
    ord = Order(**data)
    assert ord.id == "O1001"
    assert ord.lmt_price == 150.0
