# from getpass import getpass
import time

import grpc

import bisq.api.grpc_pb2 as bisq_messages
import bisq.api.grpc_pb2_grpc as bisq_service


class EditOffer:

    def __init__(self, offer_id):
        self.offerid = offer_id

    def disable_offer_request(self):
        return bisq_messages.EditOfferRequest(
            id=self.offerid,
            edit_type=bisq_messages.EditOfferRequest.EditType.ACTIVATION_STATE_ONLY,
            enable=0)  # If enable=-1: ignore enable param, enable=0: disable offer, enable=1: enable offer

    def enable_offer_request(self):
        return bisq_messages.EditOfferRequest(
            id=self.offerid,
            edit_type=bisq_messages.EditOfferRequest.EditType.ACTIVATION_STATE_ONLY,
            enable=1)  # If enable=-1: ignore enable param, enable=0: disable offer, enable=1: enable offer

    def main(self):
        grpc_channel = grpc.insecure_channel('localhost:9998')
        grpc_service_stub = bisq_service.OffersStub(grpc_channel)
        api_password: str = 'xyz'  # getpass("Enter API password: ")
        try:
            edit_offer_request = self.disable_offer_request()
            edit_offer_response = grpc_service_stub.EditOffer.with_call(edit_offer_request,
                                                                        metadata=[('password', api_password)])
            print('Offer is disabled.  Rpc response: ' + str(edit_offer_response))
            time.sleep(4)  # Wait for new offer preparation and wallet updates before creating another offer.

            edit_offer_request = self.enable_offer_request()
            edit_offer_response = grpc_service_stub.EditOffer.with_call(edit_offer_request,
                                                                        metadata=[('password', api_password)])
            print('Offer is enabled.  Rpc response: ' + str(edit_offer_response))
            time.sleep(4)  # Wait for new offer preparation and wallet updates before creating another offer.

            edit_offer_request = self.edit_fixed_price_request()
            edit_offer_response = grpc_service_stub.EditOffer.with_call(edit_offer_request,
                                                                        metadata=[('password', api_password)])
            print('Offer fixed-price has been changed.  Rpc response: ' + str(edit_offer_response))
            time.sleep(4)  # Wait for new offer preparation and wallet updates before creating another offer.

            edit_offer_request = self.edit_fixed_price_and_enable_request()
            edit_offer_response = grpc_service_stub.EditOffer.with_call(edit_offer_request,
                                                                        metadata=[('password', api_password)])
            print('Offer fixed-price has been changed, and offer is enabled.  Rpc response: ' + str(edit_offer_response))
            time.sleep(4)  # Wait for new offer preparation and wallet updates before creating another offer.

            # Change the fixed-price offer to a mkt price margin based offer
            edit_offer_request = self.edit_price_margin_request()
            edit_offer_response = grpc_service_stub.EditOffer.with_call(edit_offer_request,
                                                                        metadata=[('password', api_password)])
            print('Fixed-price offer is not a mkt price margin based offer.  Rpc response: ' + str(edit_offer_response))
            time.sleep(4)  # Wait for new offer preparation and wallet updates before creating another offer.

            # Set the trigger-price on a mkt price margin based offer
            edit_offer_request = self.edit_trigger_price_request()
            edit_offer_response = grpc_service_stub.EditOffer.with_call(edit_offer_request,
                                                                        metadata=[('password', api_password)])
            print('Offer trigger price is set.  Rpc response: ' + str(edit_offer_response))

        except grpc.RpcError as rpc_error:
            print('gRPC API Exception: %s', rpc_error)

    def edit_fixed_price_request(self):
        return bisq_messages.EditOfferRequest(
            id=self.offerid,
            price='12000.50',
            edit_type=bisq_messages.EditOfferRequest.EditType.FIXED_PRICE_ONLY,
            enable=-1)  # If enable=-1: ignore enable param, enable=0: disable offer, enable=1: enable offer

    def edit_fixed_price_and_enable_request(self):
        return bisq_messages.EditOfferRequest(
            id=self.offerid,
            price='43000.50',
            edit_type=bisq_messages.EditOfferRequest.EditType.FIXED_PRICE_AND_ACTIVATION_STATE,
            enable=1)  # If enable=-1: ignore enable param, enable=0: disable offer, enable=1: enable offer

    def edit_price_margin_request(self):
        return bisq_messages.EditOfferRequest(
            id=self.offerid,
            use_market_based_price=True,
            market_price_margin_pct=5.00,
            edit_type=bisq_messages.EditOfferRequest.EditType.MKT_PRICE_MARGIN_ONLY,
            enable=-1)  # If enable=-1: ignore enable param, enable=0: disable offer, enable=1: enable offer

    def edit_trigger_price_request(self):
        return bisq_messages.EditOfferRequest(
            id=self.offerid,
            trigger_price='40000.0000',
            edit_type=bisq_messages.EditOfferRequest.EditType.TRIGGER_PRICE_ONLY,
            enable=-1)  # If enable=-1: ignore enable param, enable=0: disable offer, enable=1: enable offer
