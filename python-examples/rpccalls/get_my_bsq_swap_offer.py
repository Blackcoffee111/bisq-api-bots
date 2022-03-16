from builtins import print

import grpc

# from getpass import getpass
import bisq.api.grpc_pb2 as bisq_messages
import bisq.api.grpc_pb2_grpc as bisq_service


def main():
    grpc_channel = grpc.insecure_channel('localhost:9998')
    grpc_service_stub = bisq_service.OffersStub(grpc_channel)
    api_password: str = 'xyz'  # getpass("Enter API password: ")
    try:
        response = grpc_service_stub.GetMyBsqSwapOffer.with_call(
            bisq_messages.GetMyOfferRequest(id='gzcvxum-63c23b0b-6acd-49ba-a956-55e406994da1-184'),
            metadata=[('password', api_password)])
        print('Response: ' + str(response[0].bsq_swap_offer))
    except grpc.RpcError as rpc_error:
        print('gRPC API Exception: %s', rpc_error)


if __name__ == '__main__':
    main()
