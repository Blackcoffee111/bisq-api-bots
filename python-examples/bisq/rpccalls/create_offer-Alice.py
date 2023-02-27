from google.protobuf.json_format import MessageToJson
import json
import grpc
import time
import bisq.api.grpc_pb2 as bisq_messages
import bisq.api.grpc_pb2_grpc as bisq_service


# Bob orders
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


payment_account_id = "94c80b96-628d-4fa5-a9f6-616531631ae8"
password = "xyz"
direction = "SELL"
currency_code = "EUR"
localhost = 'localhost:9998'

grpc_channel = grpc.insecure_channel(localhost)

# for i in range(4):
#     price = str(10000*(i+1))
send_order(False, margin=1, amount=2000000, min_amount=100000, security_deposit=15, fee_currency="BSQ")
