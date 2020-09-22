from Models.Block import Block as BaseBlock

# This virtual block is in fact not a block, but 2**r blocks (described in B++) 
class VirtualBlock(BaseBlock):

    """ Defines the B++ Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    :param int courage: the constant which determines the number of forks after B++ explodes
    :param int risk_level: the variable which means there are 2**risk_level blocks being mined in this interval
    """

    def __init__(self,
	 depth=0,
	 id=0,
	 previous=-1,
	 timestamp=0,
	 miner=None,
	 transactions=[],
	 size=1.0,
	 courage=0,
     risk_level=0,
     blocks=[]):

        super().__init__(depth,id,previous,timestamp,miner,transactions,size)
        self.courage= courage
        self.risk_level= risk_level
        self.block_num= 2**risk_level
        self.blocks= [None for i in range(self.block_num)]

    def insert_block(block, branch_id):
        self.blocks[branch_id]= block
    
    def is_interval_finished():
        return self.blocks.count(None) == 0

class RealBlock(BaseBlock):
    """ Defines the B++ Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    :param int courage: the constant which determines the number of forks after B++ explodes
    :param int risk_level: the variable which means there are 2**risk_level blocks being mined in this interval
    """

    def __init__(self,
	 depth=0,
	 id=0,
	 previous=-1,
	 timestamp=0,
	 miner=None,
	 transactions=[],
	 size=1.0,
	 courage=0,
     risk_level=0,
     branch_id=0):

        super().__init__(depth,id,previous,timestamp,miner,transactions,size)
        self.courage= courage
        self.risk_level= risk_level
        self.branch_id = branch_id# TODO: If the method of distributing miners described in section III. should be implemented