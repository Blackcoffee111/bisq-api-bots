#!/bin/bash
source "env.sh"
$BISQ_HOME/bisq-cli --password=xyz --port=9998 unlockwallet --wallet-password=abc --timeout=30
