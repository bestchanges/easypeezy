import vcr

from decider import core
from decider.core import Node
from providers import c2c
from tests.testutils import cassette

search_item = {
    "adv": {
        "advNo": "11372091689796468736",
        "classify": "mass",
        "tradeType": "SELL",
        "asset": "USDT",
        "fiatUnit": "KZT",
        "advStatus": None,
        "priceType": None,
        "priceFloatingRatio": None,
        "rateFloatingRatio": None,
        "currencyRate": None,
        "price": "456.84",
        "initAmount": "27507.41000000",
        "surplusAmount": "408.18",
        "amountAfterEditing": "9696.13000000",
        "maxSingleTransAmount": "4500000.00",
        "minSingleTransAmount": "70000.00",
        "buyerKycLimit": None,
        "buyerRegDaysLimit": None,
        "buyerBtcPositionLimit": None,
        "remarks": None,
        "autoReplyMsg": "",
        "payTimeLimit": 15,
        "tradeMethods": [
            {
                "payId": None,
                "payMethodId": "",
                "payType": "HalykBank",
                "payAccount": None,
                "payBank": None,
                "paySubBank": None,
                "identifier": "HalykBank",
                "iconUrlColor": "https://bin.bnbstatic.com/image/admin_mgs_image_upload/20201023/500c91ef-fb9e-48be-ba8b-43c1fc62a7a6.png",
                "tradeMethodName": "Halyk Bank",
                "tradeMethodShortName": "Halyk Bank",
                "tradeMethodBgColor": "#00805F",
            }
        ],
        "userTradeCountFilterTime": None,
        "userBuyTradeCountMin": None,
        "userBuyTradeCountMax": None,
        "userSellTradeCountMin": None,
        "userSellTradeCountMax": None,
        "userAllTradeCountMin": None,
        "userAllTradeCountMax": None,
        "userTradeCompleteRateFilterTime": None,
        "userTradeCompleteCountMin": None,
        "userTradeCompleteRateMin": None,
        "userTradeVolumeFilterTime": None,
        "userTradeType": None,
        "userTradeVolumeMin": None,
        "userTradeVolumeMax": None,
        "userTradeVolumeAsset": None,
        "createTime": None,
        "advUpdateTime": None,
        "fiatVo": None,
        "assetVo": None,
        "advVisibleRet": None,
        "assetLogo": None,
        "assetScale": 2,
        "fiatScale": 2,
        "priceScale": 2,
        "fiatSymbol": "〒",
        "isTradable": True,
        "dynamicMaxSingleTransAmount": "186286.66",
        "minSingleTransQuantity": "153.22",
        "maxSingleTransQuantity": "9850.27",
        "dynamicMaxSingleTransQuantity": "407.77",
        "tradableQuantity": "407.77",
        "commissionRate": "0.00100000",
        "tradeMethodCommissionRates": [],
        "launchCountry": None,
    },
    "advertiser": {
        "userNo": "s853153fcbfa8359a9e9123e9dd6353cd",
        "realName": None,
        "nickName": "-VISA-MASTERCARD-",
        "margin": None,
        "marginUnit": None,
        "orderCount": None,
        "monthOrderCount": 260,
        "monthFinishRate": 1.0,
        "advConfirmTime": 0,
        "email": None,
        "registrationTime": None,
        "mobile": None,
        "userType": "user",
        "tagIconUrls": [],
        "userGrade": 2,
        "userIdentity": "",
        "proMerchant": None,
        "isBlocked": None,
    },
}

# https://c2c.binance.com/bapi/c2c/v2/friendly/
r = {
    "code": "000000",
    "message": None,
    "messageDetail": None,
    "data": {
        "fiat": "CNY",
        "areas": [
            {
                "area": "EXPRESS",
                "proMerchantFilterAvailable": False,
                "tradeSides": [
                    {
                        "side": "BUY",
                        "assets": [
                            {
                                "asset": "USDT",
                                "description": "Tether",
                                "iconUrl": None,
                            },
                            {
                                "asset": "BTC",
                                "description": "Bitcoin",
                                "iconUrl": None,
                            },
                            {
                                "asset": "BUSD",
                                "description": "Binance USD",
                                "iconUrl": None,
                            },
                            {
                                "asset": "BNB",
                                "description": "Binance Coin",
                                "iconUrl": None,
                            },
                            {
                                "asset": "DOGE",
                                "description": "Dogecoin",
                                "iconUrl": None,
                            },
                            {
                                "asset": "ETH",
                                "description": "Ethereum",
                                "iconUrl": None,
                            },
                        ],
                        "convertAssets": [],
                        "tradeMethods": [
                            {"identifier": "BANK"},
                            {"identifier": "ALIPAY"},
                            {"identifier": "WECHAT"},
                        ],
                    },
                    {
                        "side": "SELL",
                        "assets": [
                            {
                                "asset": "USDT",
                                "description": "Tether",
                                "iconUrl": None,
                            },
                            {
                                "asset": "BTC",
                                "description": "Bitcoin",
                                "iconUrl": None,
                            },
                            {
                                "asset": "BUSD",
                                "description": "Binance USD",
                                "iconUrl": None,
                            },
                            {
                                "asset": "BNB",
                                "description": "Binance Coin",
                                "iconUrl": None,
                            },
                            {
                                "asset": "DOGE",
                                "description": "Dogecoin",
                                "iconUrl": None,
                            },
                            {
                                "asset": "ETH",
                                "description": "Ethereum",
                                "iconUrl": None,
                            },
                        ],
                        "convertAssets": [],
                        "tradeMethods": [
                            {"identifier": "BANK"},
                            {"identifier": "ALIPAY"},
                            {"identifier": "WECHAT"},
                        ],
                    },
                ],
            },
            {
                "area": "BLOCK",
                "proMerchantFilterAvailable": False,
                "tradeSides": [
                    {
                        "side": "BUY",
                        "assets": [
                            {"asset": "USDT", "description": None, "iconUrl": None},
                            {"asset": "BUSD", "description": None, "iconUrl": None},
                            {"asset": "BTC", "description": None, "iconUrl": None},
                            {"asset": "ETH", "description": None, "iconUrl": None},
                            {"asset": "BNB", "description": None, "iconUrl": None},
                        ],
                        "convertAssets": [],
                        "tradeMethods": [
                            {"identifier": "ALIPAY"},
                            {"identifier": "BANK"},
                            {"identifier": "WECHAT"},
                        ],
                    },
                    {
                        "side": "SELL",
                        "assets": [
                            {"asset": "USDT", "description": None, "iconUrl": None},
                            {"asset": "BUSD", "description": None, "iconUrl": None},
                            {"asset": "BTC", "description": None, "iconUrl": None},
                            {"asset": "ETH", "description": None, "iconUrl": None},
                            {"asset": "BNB", "description": None, "iconUrl": None},
                        ],
                        "convertAssets": [],
                        "tradeMethods": [
                            {"identifier": "ALIPAY"},
                            {"identifier": "BANK"},
                            {"identifier": "WECHAT"},
                        ],
                    },
                ],
            },
            {
                "area": "P2P",
                "proMerchantFilterAvailable": False,
                "tradeSides": [
                    {
                        "side": "BUY",
                        "assets": [
                            {"asset": "USDT", "description": None, "iconUrl": None},
                            {"asset": "BTC", "description": None, "iconUrl": None},
                            {"asset": "BUSD", "description": None, "iconUrl": None},
                            {"asset": "BNB", "description": None, "iconUrl": None},
                            {"asset": "ETH", "description": None, "iconUrl": None},
                            {"asset": "DOGE", "description": None, "iconUrl": None},
                            {"asset": "DAI", "description": None, "iconUrl": None},
                        ],
                        "convertAssets": [],
                        "tradeMethods": [],
                    },
                    {
                        "side": "SELL",
                        "assets": [
                            {"asset": "USDT", "description": None, "iconUrl": None},
                            {"asset": "BTC", "description": None, "iconUrl": None},
                            {"asset": "BUSD", "description": None, "iconUrl": None},
                            {"asset": "BNB", "description": None, "iconUrl": None},
                            {"asset": "ETH", "description": None, "iconUrl": None},
                            {"asset": "DOGE", "description": None, "iconUrl": None},
                            {"asset": "DAI", "description": None, "iconUrl": None},
                        ],
                        "convertAssets": [],
                        "tradeMethods": [],
                    },
                ],
            },
        ],
        "filterDefaultValues": {"publisherType": ""},
    },
    "success": True,
}


@vcr.use_cassette(cassette("cassettes/tests/binance_c2c_buy_kzt.yaml"))
def test_load_binance_c2c_offers_buy_kzt():
    fiat = "KZT"
    trade_type = "BUY"
    offers = c2c.load_binance_c2c_offers(fiat, trade_type)
    assert set(offers) == {"USDT", "BTC", "BUSD", "BNB", "ETH", "SHIB"}
    for asset, offers in offers.items():
        assert 0 < len(offers) <= 10


@vcr.use_cassette(cassette("cassettes/tests/binance_c2c_sell_rub.yaml"))
def test_load_binance_c2c_offers_sell_rub():
    fiat = "RUB"
    trade_type = "SELL"
    offers = c2c.load_binance_c2c_offers(fiat, trade_type)
    assert set(offers) == {"USDT", "BTC", "BUSD", "BNB", "ETH", "SHIB", "RUB"}
    for asset, offers in offers.items():
        assert len(offers) <= 10


@vcr.use_cassette(cassette("cassettes/tests/binance_c2c_sell_rub.yaml"))
def test_add_to_graph_sell_rub():
    graph = core.Graph()
    offers = c2c.load_binance_c2c_offers(fiat="RUB", trade_type="SELL")

    c2c.add_c2c_offers_to_graph(offers["USDT"], graph)

    fiat_node = core.Node(currency="RUB(f)")
    asset_node = core.Node(currency="USDT")
    assert graph._nodes == {fiat_node, asset_node}
    # TODO: round result
    assert len(graph._edges) == 1
    edge = graph._edges[0]  # type:c2c.BinnanceP2PEdge
    assert type(edge) == c2c.BinnanceP2PEdge
    assert edge.commission() == 0
    assert edge.converted() == 61.349999999999994
    assert edge.from_ == fiat_node
    assert edge.to == asset_node
    assert edge.url() == 'https://c2c.binance.com/ru/trade/sell/USDT?fiat=RUB&payment=ALL'

@vcr.use_cassette(cassette("cassettes/tests/binance_c2c_buy_kzt.yaml"))
def test_add_to_graph_buy_kzt():
    offers = c2c.load_binance_c2c_offers(fiat="KZT", trade_type="BUY")

    graph = core.Graph()
    c2c.add_c2c_offers_to_graph(offers["USDT"], graph)

    fiat_node = core.Node(currency="KZT(f)")
    asset_node = core.Node(currency="USDT")
    assert graph._nodes == {fiat_node, asset_node}

    assert len(graph._edges) == 1
    edge = graph._edges[0]  # type:c2c.BinnanceP2PEdge
    assert type(edge) == c2c.BinnanceP2PEdge
    assert edge.commission() == 0
    assert edge.converted() == 0.0021599671684990386
    assert edge.from_ == asset_node
    assert edge.to == fiat_node
    assert edge.url() == 'https://c2c.binance.com/ru/trade/all-payments/USDT?fiat=KZT'


@vcr.use_cassette(cassette("cassettes/tests/c2c_test_add_to_graph_all.yaml"))
def test_add_to_graph_all():
    graph = core.Graph()
    offers_1 = c2c.load_binance_c2c_offers(fiat="KZT", trade_type="BUY")
    offers_2 = c2c.load_binance_c2c_offers(fiat="RUB", trade_type="SELL")

    for asset_offers in list(offers_1.values()) + list(offers_2.values()):
        c2c.add_c2c_offers_to_graph(asset_offers, graph)

    assert graph._nodes == {
        Node(currency="BUSD"),
        Node(currency="BNB"),
        Node(currency="ETH"),
        Node(currency="BTC"),
        Node(currency="RUB"),
        Node(currency="SHIB"),
        Node(currency="KZT(f)"),
        Node(currency="USDT"),
        Node(currency="RUB(f)"),
    }
    assert 13, len(graph._edges)
