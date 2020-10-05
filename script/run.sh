#!/bin/sh

set -aeo pipefail

# file path
DIR_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
DIR_OUTPUT="${DIR_ROOT}/output"

# util script
source "${DIR_ROOT}/script/util.sh"

# script option
MODEL_NAMES=(base bitcoin ethereum b++)

# global variable
MODEL_NAME=
MODEL=

# function_exists checks whether function declared
function function_exists() {
    declare -f -F "${1}" > /dev/null
    return $?
}

# model_id get model's id from model name
function model_id {
    for i in ${!MODEL_NAMES[@]}; do
        if [ "${MODEL_NAMES[$i]}" = "${1}" ]; then
            echo $i
            return 0
        fi
    done
    echo -1
}

# run runs main program
function run {
    OUTPUT=${OUTPUT:-"${DIR_OUTPUT}/${MODEL_NAME}"}
    python3 "${DIR_ROOT}/Main.py"
}

function run_different_node_count {
    for NODE_COUNT in `seq 1 10`; do
        NODE_COUNT="${NODE_COUNT}0"
        NODE_HASH_POWER=$(join_by_comma $(for i in $(seq 1 "${NODE_COUNT}"); do echo 1; done))
        OUTPUT="${DIR_OUTPUT}/${MODEL_NAME}-node-count-${NODE_COUNT}"
        run
    done
}

function main {
    # prepare model id
    MODEL_NAME=${1}
    MODEL=`model_id ${MODEL_NAME}`
    if [ ${MODEL} -eq -1 ]; then
        printf 'please specify model in\n'
        printf '* %s\n' "${MODEL_NAMES[@]}"
        exit 1
    fi

    # source env
    local ENV_FILE=".env.${MODEL_NAME}"
    [[ ! -f $ENV_FILE ]] && printf 'model has no env file yet\n' && exit 1
    source $ENV_FILE

    # source runnable script
    local MODEL_RUNNABLE_FILE="${DIR_ROOT}/script/run_${MODEL_NAME}.sh"
    [[ -f $MODEL_RUNNABLE_FILE ]] && source ${MODEL_RUNNABLE_FILE}

    # run
    local RUN=${2}
    if ! function_exists ${RUN}; then
        FUNCTIONS=(`declare -F | awk '{print $3}' | grep --invert-match 'function_exists\|main\|model_id\|join_by\|join_by_comma'`)
        printf 'please specify function in\n'
        printf '* %s\n' "${FUNCTIONS[@]}"
        exit 1
    fi
    eval ${RUN}
}

main $@
