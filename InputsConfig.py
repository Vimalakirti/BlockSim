import os
import sys

''' Seclect the model to be simulated.
0 : The base model
1 : Bitcoin model
2 : Ethereum model
3 : B++ model
'''
model = int(os.getenv('MODEL', 0))

if model == 0:
    from Models.Node import Node
elif model == 1:
    from Models.Bitcoin.Node import Node
elif model == 2:
    from Models.Ethereum.Node import Node
elif model == 3:
    from Models.Bplusplus.Node import Node

class InputsConfig:

    model = model

    ''' Block Parameters '''
    # average time for creating a block in the blockchain
    Binterval = float(os.getenv('BLOCK_INTERVAL', 600))
    # block size in MB
    Bsize = float(os.getenv('BLOCK_SIZE', 1.0))
    # average block propogation delay in seconds, ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw
    Bdelay = float(os.getenv('BLOCK_PROPAGATION_DELAY', 0.42))
    # reward for mining a block
    Breward = float(os.getenv('BLOCK_REWARD', 12.5))

    ''' Transaction Parameters '''
    # whether to enable transactions in the simulator
    hasTrans = bool(os.getenv('TRANSACTION_ENABLED', True))
    # specify the way of modelling transactions {Full, Light}
    Ttechnique = os.getenv('TRANSACTION_TECHNIQUE', 'Light')
    # average transaction size in MB
    Tsize = float(os.getenv('TRANSACTION_SIZE', 0.000546))
    # rate of the number of transactions to be created per second
    Tn = int(os.getenv('TRANSACTION_PER_SECOND', 10))
    # average transaction propagation delay in seconds (Only if Full technique is used)
    Tdelay = float(os.getenv('TRANSACTION_PROPAGATION_DELAY', 5.1))
    # average transaction fee
    Tfee = float(os.getenv('TRANSACTION_FEE', 0.000062))

    ''' Node Parameters '''
    # total count of nodes in the network
    NODES = []
    Nn = int(os.getenv('NODE_COUNT', 3))
    Npower = os.getenv('NODE_HASH_POWER', '50,20,30')
    node_hash_powers = [float(node_hash_power)
                        for node_hash_power in Npower.split(',')]
    if len(node_hash_powers) != Nn:
        sys.exit('length of node hash powers must be equal to node count %d, but got %d' % (
            Nn, len(node_hash_powers)))
    if sum(node_hash_powers) != 100:
        sys.exit('sum of node hash powers must be 100, but got %f' %
                 sum(node_hash_powers))

    ''' Simulation Parameters '''
    # simulation length (in seconds)
    simTime = int(os.getenv('SIMULATION_TIME', 1000))
    # count of simulation runs
    Runs = int(os.getenv('SIMULATION_RUN', 3))

    ''' Base '''
    if model == 0:
        NODES = [Node(id=i) for i in range(Nn)]

    ''' Bitcoin '''
    if model == 1:
        NODES = [Node(id=id, hashPower=hash_power)
                 for id, hash_power in enumerate(node_hash_powers)]

    ''' Ethereum '''
    if model == 2:
        # The block gas limit
        Blimit = int(os.getenv('BLOCK_GAS_LIMIT', 8000000))
        # whether to enable uncle in the simulator
        hasUncles = bool(os.getenv('UNCLE_ENABLED', True))
        # max count of uncle blocks allowed per block
        Buncles = int(os.getenv('UNCLE_PER_BLOCK', 2))
        # depth in which an uncle can be included in a block
        Ugenerations = int(os.getenv('UNCLE_DEPTH', 7))
        # reward for an uncle block
        Ureward = int(os.getenv('UNCLE_REWARD', 0))
        # reward for including an uncle
        UIreward = float(os.getenv('UNCLE_INCLUDING_REWARD', Breward / 32))

        NODES = [Node(id=id, hashPower=hash_power)
                 for id, hash_power in enumerate(node_hash_powers)]

    ''' B++ '''
    if model == 3:
        Bdmin = int(os.getenv('BLOCK_D_MIN', -3))

        NODES = [Node(id=id, hashPower=hash_power)
                 for id, hash_power in enumerate(node_hash_powers)]
