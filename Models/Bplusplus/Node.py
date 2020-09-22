from Models.Block import Block
from Models.Node import Node as BaseNode

class Node(BaseNode):
    def __init__(self,id,hashPower,courage):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id)#,blockchain,transactionsPool,blocks,balance)
        self.hashPower = hashPower
        self.blockchain= []# create an array for each miner to store chain state locally
        self.transactionsPool= []
        self.blocks= 0# total number of blocks mined in the main chain
        self.balance= 0# to count all reward that a miner made, including block rewards + uncle rewards + transactions fees
        self.branchId= 0# TODO: If the method of distributing miners described in section III. should be implemented
        self.risk_level= 0
        self.courage= courage

    def update_finite_state_machine(self):
        if self.security_level == 0:
            self.security_level = self.d_min # Explode
        else:
            self.security_level += 1 # Merge

    def get_block_num(self):
        return 2**self.security_level