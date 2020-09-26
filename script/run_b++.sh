#!/bin/sh

function run_different_dmin {
    for BLOCK_D_MIN in `seq 0 10`; do
        OUTPUT="${DIR_OUTPUT}/${MODEL_NAME}-dmin-${BLOCK_D_MIN}"
        BLOCK_D_MIN="-${BLOCK_D_MIN}"
        run
    done
}
