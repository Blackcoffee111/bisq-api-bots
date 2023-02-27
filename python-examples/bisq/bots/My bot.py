from google.protobuf.json_format import MessageToJson
import json
import grpc
import time
import bisq.api.grpc_pb2 as bisq_messages
import bisq.api.grpc_pb2_grpc as bisq_service


def send_order(fixed: bool, amount: int, min_amount: int, security_deposit: int,
               fee_currency: str, price: str = "", margin: float = 0.0):
    try:
        if not fixed:
            create_offer_request = bisq_messages.CreateOfferRequest(direction=direction,
                                                                    currency_code=currency_code,
                                                                    use_market_based_price=True,
                                                                    market_price_margin_pct=margin,
                                                                    amount=amount,
                                                                    min_amount=min_amount,
                                                                    buyer_security_deposit_pct=security_deposit,
                                                                    payment_account_id=payment_account_id,
                                                                    maker_fee_currency_code=fee_currency)
        if fixed:
            create_offer_request = bisq_messages.CreateOfferRequest(direction=direction,
                                                                    currency_code=currency_code,
                                                                    price=price,
                                                                    amount=amount,
                                                                    min_amount=min_amount,
                                                                    buyer_security_deposit_pct=security_deposit,
                                                                    payment_account_id=payment_account_id,
                                                                    maker_fee_currency_code=fee_currency)

        create_offer_response = bisq_service.OffersStub(grpc_channel).CreateOffer.with_call(create_offer_request,
                                                                                            metadata=[
                                                                                                ('password', password)])
        print('New order: ' + str(create_offer_response[0].offer))
    except grpc.RpcError as rpc_error:
        print('gRPC API Exception: %s', rpc_error)


def get_all_offers():
    try:
        response = bisq_service.OffersStub(grpc_channel).GetOffers.with_call(
            bisq_messages.GetOffersRequest(
                direction=direction,
                currency_code=currency_code),
            metadata=[('password', password)])
        data = MessageToJson(response[0])
        offers = json.loads(data)
        if not offers:
            return None
        offers = offers['offers']
        return offers
    except grpc.RpcError as rpc_error:
        print('gRPC API Exception: %s', rpc_error)


def get_my_offers():
    try:
        response = bisq_service.OffersStub(grpc_channel).GetMyOffers.with_call(
            bisq_messages.GetMyOffersRequest(
                direction=direction,
                currency_code=currency_code),
            metadata=[('password', password)])
        data = MessageToJson(response[0])
        offers = json.loads(data)
        if not offers:
            return None
        offers = offers['offers']
        return offers
    except grpc.RpcError as rpc_error:
        print('gRPC API Exception: %s', rpc_error)


# Initial Parameters:

payment_account_id = "94c80b96-628d-4fa5-a9f6-616531631ae8"
password = "xyz"
direction = "SELL"
currency_code = "EUR"
localhost = 'localhost:9998'
min_margin = 2
margin = 5
grpc_channel = grpc.insecure_channel(localhost)


# send_order(False, margin=2, amount=3000000, min_amount=1500000, security_deposit=15, fee_currency="BSQ")

while True:
    myoffers = get_my_offers()
    if not myoffers:
        print("No offers")
        time.sleep(60)
        continue
    for i in myoffers:
        print(f"{i['direction']} - {i['price']} - {i['amount']} - {i['paymentAccountId']} - {i['id']}")

    alloffers = get_all_offers()
    for i in alloffers:
        print(f"{i['direction']} - {i['price']} - {i['amount']} - {i['paymentAccountId']} - {i['id']}")
    time.sleep(60)