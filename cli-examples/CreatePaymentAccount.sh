#!/bin/bash
source "env.sh"
# Create a swift fiat payment account, providing details in a json form generated by getpaymentacctform.
$BISQ_HOME/bisq-cli --password=xyz --port=9998 createpaymentacct --payment-account-form=swift.json
