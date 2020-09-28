from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c

class Incentives:
    def distribute_rewards():
        node_by_id = {node.id: node for node in p.NODES}
        for block in c.global_chain:
            for branch in block.branches:
                if branch.miner == None:
                    continue
                node_by_id[branch.miner].blocks +=1
                reward = p.Breward
                if block.security_level() < 0:
                    reward /= abs(block.security_level())
                node_by_id[branch.miner].balance += reward
                node_by_id[branch.miner].balance += sum([tx.fee for tx in branch.transactions])
