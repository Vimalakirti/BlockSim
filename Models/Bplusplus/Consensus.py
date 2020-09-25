import numpy as np
from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as BaseConsensus
import random


class Consensus(BaseConsensus):

    """
	We modelled PoW consensus protocol by drawing the time it takes the miner to finish the PoW from an exponential distribution
        based on the invested hash power (computing power) fraction
    """
    def Protocol(miner):
        ##### Start solving a fresh PoW on top of last block appended #####
        TOTAL_HASHPOWER = sum([miner.hashPower for miner in p.NODES])
        hashPower = miner.hashPower/TOTAL_HASHPOWER
        security_level_factor = 2**miner.next_unfinished_virtual_block().security_level()
        return random.expovariate(hashPower / (p.Binterval * security_level_factor))

    """
	This method apply the longest-chain approach to resolve the forks that occur when nodes have multiple differeing copies of the blockchain ledger
    """
    def fork_resolution():
        BaseConsensus.global_chain = []  # reset the global chain before filling it

        depths = [node.last_finished_virtual_block().depth for node in p.NODES]
        longest_chain_node_idx = depths.index(max(depths))
        
        for block in p.NODES[longest_chain_node_idx].blockchain:
            if not block.is_finished():
                break

            for branch in block.branches:
                block.transactions += branch.transactions
            BaseConsensus.global_chain.append(block)
