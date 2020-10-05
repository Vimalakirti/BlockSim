import random
from Models.Bplusplus.Block import VirtualBlock, Block
from Models.Node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, id, hashPower):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id)  # ,blockchain,transactionsPool,blocks,balance)
        self.hashPower = hashPower
        self.blockchain = []  # create an array for each miner to store chain state locally
        self.transactionsPool = []
        self.blocks = 0  # total number of blocks mined in the main chain
        self.balance = 0  # to count all reward that a miner made, including block rewards + uncle rewards + transactions fees
        self.mining_branch = None

    def generate_gensis_block():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            vblock = VirtualBlock()
            vblock.set_branch(Block())
            node.blockchain.append(vblock)

    def resetState():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain = []
            node.transactionsPool = []
            node.blocks = 0
            node.balance = 0

    def next_unfinished_virtual_block(self):
        next_unfinished_virtual_block_depth = self.last_finished_virtual_block().depth + 1
        self.grow_blockchain(next_unfinished_virtual_block_depth)
        return self.blockchain[next_unfinished_virtual_block_depth]

    def last_finished_virtual_block(self):
        for block in reversed(self.blockchain):
            if block.is_finished():
                return block

    def grow_blockchain(self, depth):
        current_depth = len(self.blockchain) - 1
        if current_depth < depth:
            for i in range(depth - current_depth):
                new_block_depth = current_depth + 1 + i
                self.blockchain.append(
                    VirtualBlock(
                        id=new_block_depth,
                        depth=new_block_depth,
                        previous=new_block_depth-1,
                    )
                )
