#!/bin/sh

function run_different_dmin {
    for BLOCK_D_MIN in `seq 0 10`; do
        OUTPUT="${DIR_OUTPUT}/${MODEL_NAME}-dmin-${BLOCK_D_MIN}"
        BLOCK_D_MIN="-${BLOCK_D_MIN}"
        run
    done
}

# when dmin is set to zero, b++'s behavior will be exactly like bitcoin
function run_as_bitcoin {
    OUTPUT="${DIR_OUTPUT}/${MODEL_NAME}-as-bitcoin"
    BLOCK_D_MIN="0"
    run
}
