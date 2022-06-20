import logging
import statistics
from decimal import Decimal
from typing import List, Dict

import requests

import core

logger = logging.getLogger(__name__)


def binance_c2c_search(session: requests.Session, fiat: str, asset: str, trade_type: str, pay_types=(), countries=(), publisher_type=None, rows=10, page=1):
    """
    Search for C2C offers.

    :param fiat: fiat currency like 'KZT'
    :param asset: crypto currency like 'USDT'
    :param trade_type: 'BUY' or 'SELL' crypto for fiat
    :param pay_types: list of strings payment types, like ["KaspiBank"]
    :param countries: list of strings countries like ["KZ"]
    :param publisher_type: None for any, 'merchant' for only from merchants.
    :param rows: number or items to return
    :param page: page number. Starts with 1.
    :return: 
    """
    assert fiat
    assert asset
    assert trade_type in ('BUY', 'SELL')
    request_payload = {
        "page": page,
        "rows": rows,
        "payTypes": pay_types,
        "countries": countries,
        "publisherType": publisher_type,
        "asset": asset,
        "fiat": fiat,
        "tradeType": trade_type
    }
    r = session.post('https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=request_payload)
    r.raise_for_status()
    response_payload = r.json()
    item = {
        'adv': {
            'advNo': '11372091689796468736',
            'classify': 'mass', 'tradeType': 'SELL', 'asset': 'USDT',
            'fiatUnit': 'KZT', 'advStatus': None, 'priceType': None, 'priceFloatingRatio': None,
            'rateFloatingRatio': None, 'currencyRate': None, 'price': '456.84',
            'initAmount': '27507.41000000', 'surplusAmount': '408.18', 'amountAfterEditing': '9696.13000000',
            'maxSingleTransAmount': '4500000.00', 'minSingleTransAmount': '70000.00', 'buyerKycLimit': None,
            'buyerRegDaysLimit': None, 'buyerBtcPositionLimit': None, 'remarks': None, 'autoReplyMsg': '',
            'payTimeLimit': 15, 'tradeMethods': [
                {'payId': None, 'payMethodId': '', 'payType': 'HalykBank', 'payAccount': None, 'payBank': None,
                 'paySubBank': None, 'identifier': 'HalykBank',
                 'iconUrlColor': 'https://bin.bnbstatic.com/image/admin_mgs_image_upload/20201023/500c91ef-fb9e-48be-ba8b-43c1fc62a7a6.png',
                 'tradeMethodName': 'Halyk Bank', 'tradeMethodShortName': 'Halyk Bank', 'tradeMethodBgColor': '#00805F'}
            ],
            'userTradeCountFilterTime': None, 'userBuyTradeCountMin': None, 'userBuyTradeCountMax': None,
            'userSellTradeCountMin': None, 'userSellTradeCountMax': None, 'userAllTradeCountMin': None,
            'userAllTradeCountMax': None, 'userTradeCompleteRateFilterTime': None, 'userTradeCompleteCountMin': None,
            'userTradeCompleteRateMin': None, 'userTradeVolumeFilterTime': None, 'userTradeType': None,
            'userTradeVolumeMin': None, 'userTradeVolumeMax': None, 'userTradeVolumeAsset': None, 'createTime': None,
            'advUpdateTime': None, 'fiatVo': None, 'assetVo': None, 'advVisibleRet': None, 'assetLogo': None, 'assetScale': 2,
            'fiatScale': 2, 'priceScale': 2, 'fiatSymbol': '〒', 'isTradable': True, 'dynamicMaxSingleTransAmount': '186286.66',
            'minSingleTransQuantity': '153.22', 'maxSingleTransQuantity': '9850.27', 'dynamicMaxSingleTransQuantity': '407.77',
            'tradableQuantity': '407.77', 'commissionRate': '0.00100000', 'tradeMethodCommissionRates': [], 'launchCountry': None
        },
        'advertiser': {
            'userNo': 's853153fcbfa8359a9e9123e9dd6353cd', 'realName': None, 'nickName': '-VISA-MASTERCARD-',
            'margin': None, 'marginUnit': None, 'orderCount': None, 'monthOrderCount': 260, 'monthFinishRate': 1.0,
            'advConfirmTime': 0, 'email': None, 'registrationTime': None, 'mobile': None, 'userType': 'user', 'tagIconUrls': [],
            'userGrade': 2, 'userIdentity': '', 'proMerchant': None, 'isBlocked': None
        }
    }
    return response_payload


def binance_c2c_config(session: requests.Session, fiat: str):
    assert fiat
    request_payload = {
        "fiat": fiat,
    }
    r = session.post('https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/portal/config', json=request_payload)
    r.raise_for_status()
    response_payload = r.json()

    # https://c2c.binance.com/bapi/c2c/v2/friendly/
    r = {
        'code': '000000', 'message': None, 'messageDetail': None,
        'data': {
            'fiat': 'CNY',
            'areas': [
                {'area': 'EXPRESS', 'proMerchantFilterAvailable': False,
                 'tradeSides': [
                     {'side': 'BUY', 'assets': [
                         {'asset': 'USDT', 'description': 'Tether', 'iconUrl': None},
                         {'asset': 'BTC', 'description': 'Bitcoin', 'iconUrl': None},
                         {'asset': 'BUSD', 'description': 'Binance USD', 'iconUrl': None},
                         {'asset': 'BNB', 'description': 'Binance Coin', 'iconUrl': None},
                         {'asset': 'DOGE', 'description': 'Dogecoin', 'iconUrl': None},
                         {'asset': 'ETH', 'description': 'Ethereum', 'iconUrl': None}],
                      'convertAssets': [],
                      'tradeMethods': [
                          {'identifier': 'BANK'},
                          {'identifier': 'ALIPAY'},
                          {'identifier': 'WECHAT'}]
                      },
                     {'side': 'SELL', 'assets': [
                         {'asset': 'USDT', 'description': 'Tether', 'iconUrl': None},
                         {'asset': 'BTC', 'description': 'Bitcoin', 'iconUrl': None},
                         {'asset': 'BUSD', 'description': 'Binance USD', 'iconUrl': None},
                         {'asset': 'BNB', 'description': 'Binance Coin', 'iconUrl': None},
                         {'asset': 'DOGE', 'description': 'Dogecoin', 'iconUrl': None},
                         {'asset': 'ETH', 'description': 'Ethereum', 'iconUrl': None}
                     ],
                      'convertAssets': [],
                      'tradeMethods': [
                          {'identifier': 'BANK'},
                          {'identifier': 'ALIPAY'},
                          {
                              'identifier': 'WECHAT'}]}]},
                {'area': 'BLOCK', 'proMerchantFilterAvailable': False,
                 'tradeSides': [
                     {'side': 'BUY', 'assets': [
                         {'asset': 'USDT', 'description': None, 'iconUrl': None},
                         {'asset': 'BUSD', 'description': None, 'iconUrl': None},
                         {'asset': 'BTC', 'description': None, 'iconUrl': None},
                         {'asset': 'ETH', 'description': None, 'iconUrl': None},
                         {'asset': 'BNB', 'description': None, 'iconUrl': None}],
                      'convertAssets': [], 'tradeMethods': [
                         {'identifier': 'ALIPAY'}, {'identifier': 'BANK'},
                         {'identifier': 'WECHAT'}]},
                     {'side': 'SELL', 'assets': [
                         {'asset': 'USDT', 'description': None, 'iconUrl': None},
                         {'asset': 'BUSD', 'description': None, 'iconUrl': None},
                         {'asset': 'BTC', 'description': None, 'iconUrl': None},
                         {'asset': 'ETH', 'description': None, 'iconUrl': None},
                         {'asset': 'BNB', 'description': None, 'iconUrl': None}
                     ], 'convertAssets': [], 'tradeMethods': [
                         {'identifier': 'ALIPAY'}, {'identifier': 'BANK'},
                         {'identifier': 'WECHAT'}]
                      }
                 ]},
                {'area': 'P2P', 'proMerchantFilterAvailable': False,
                 'tradeSides': [
                     {'side': 'BUY', 'assets': [
                         {'asset': 'USDT', 'description': None, 'iconUrl': None},
                         {'asset': 'BTC', 'description': None, 'iconUrl': None},
                         {'asset': 'BUSD', 'description': None, 'iconUrl': None},
                         {'asset': 'BNB', 'description': None, 'iconUrl': None},
                         {'asset': 'ETH', 'description': None, 'iconUrl': None},
                         {'asset': 'DOGE', 'description': None, 'iconUrl': None},
                         {'asset': 'DAI', 'description': None, 'iconUrl': None}
                     ], 'convertAssets': [], 'tradeMethods': []},
                     {'side': 'SELL', 'assets': [
                         {'asset': 'USDT', 'description': None, 'iconUrl': None},
                         {'asset': 'BTC', 'description': None, 'iconUrl': None},
                         {'asset': 'BUSD', 'description': None, 'iconUrl': None},
                         {'asset': 'BNB', 'description': None, 'iconUrl': None},
                         {'asset': 'ETH', 'description': None, 'iconUrl': None},
                         {'asset': 'DOGE', 'description': None, 'iconUrl': None},
                         {'asset': 'DAI', 'description': None, 'iconUrl': None}
                     ], 'convertAssets': [], 'tradeMethods': []}]}],
            'filterDefaultValues': {'publisherType': ''}}, 'success': True}
    return response_payload


def load_binance_c2c_offers(session: requests.Session, fiat: str, trade_type: str, max_offers=10):
    logger.info(f'Loading config for {fiat}')
    c2c_config = binance_c2c_config(
        session,
        fiat=fiat,
    )
    areas = {v['area']: v for v in c2c_config['data']['areas']}
    trade_sides = {v['side']: v for v in areas['P2P']['tradeSides']}

    asset_offers = {}
    for asset in trade_sides[trade_type]['assets']:
        asset_name = asset['asset']
        logger.info(f'Loading offers for {asset_name}')
        offers = binance_c2c_search(session, fiat=fiat, asset=asset_name, trade_type=trade_type, rows=max_offers)['data']
        logger.info(f'Loaded {len(offers)} offers for P2P {trade_type} {fiat} to {asset_name}')
        asset_offers[asset_name] = offers
    return asset_offers


def add_c2c_offers_to_graph(offers: List[Dict], graph: core.Graph, median_price_of_first_n=4):
    """
    Register C2C offers in graph.

    :param offers: list of offers. Should be same trade_type, fiat and asset currency
    :param graph:
    :param median_price_of_first_n: median value of first N items will be taken as price
    :return:
    """
    if not offers:
        return
    fiat_currency = offers[0]['adv']['fiatUnit']
    asset_currency = offers[0]['adv']['asset']
    trade_type = offers[0]['adv']['tradeType']
    assert trade_type in ('BUY', 'SELL')
    assert all([offer['adv']['tradeType'] == trade_type for offer in offers])
    assert all([offer['adv']['fiatUnit'] == fiat_currency for offer in offers])
    assert all([offer['adv']['asset'] == asset_currency for offer in offers])

    fiat_node = core.Node(currency=f'{fiat_currency}(f)')
    asset_node = core.Node(currency=asset_currency)
    graph.nodes.add(fiat_node)
    graph.nodes.add(asset_node)

    prices = [Decimal(item['adv']['price']) for item in offers]
    median_price = statistics.median(prices[:median_price_of_first_n])
    assert median_price > 0

    if trade_type == 'BUY':
        # base:USDT / quote:KZT 450    - trade_type == BUY
        # buy crypto (base) for fiat (quote)
        base = asset_node
        quote = fiat_node
        price = median_price
    else:
        # base:USDT / quote:KZT 450    - trade_type == SELL
        base = fiat_node
        quote = asset_node
        price = 1 / median_price
    edge = core.Edge(
        from_=base,
        to=quote,
        price=price,
        comission=0,
    )
    graph.edges.append(edge)
