import random
from Models.Block import Block as BaseBlock


# This virtual block is in fact not a block, but 2**r branches (described in B++)
class VirtualBlock(BaseBlock):

    """Defines the B++ Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    :param int security_level: the variable which means there are 2**security_level branches being mined in this interval
    """

    def __init__(
        self,
        depth=0,
        id=0,
        previous=-1,
        timestamp=0,
        miner=None,
        transactions=[],
        size=1.0,
    ):

        super().__init__(depth, id, previous, timestamp, miner, transactions, size)
        self.branches = [None for i in range(2**-self.security_level())]

    def security_level(self):
        from InputsConfig import InputsConfig as p
        state_count = 1-p.Bdmin
        return -((state_count - self.depth % state_count) % state_count)

    def set_branch(self, branch):
        self.branches[branch.branch_id] = branch

    def is_finished(self):
        return self.branches.count(None) == 0

    def next_branch_id(self):
        return random.choice([branch_id for branch_id, branch in enumerate(self.branches) if branch == None])

class Block(BaseBlock):

    """ Defines the base Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    """

    def __init__(
        self,
        depth=0,
        id=0,
        previous=-1,
        timestamp=0,
        miner=None,
        transactions=[],
        size=1.0,
        branch_id=0,
    ):

        super().__init__(depth, id, previous, timestamp, miner, transactions, size)
        self.branch_id = branch_id
