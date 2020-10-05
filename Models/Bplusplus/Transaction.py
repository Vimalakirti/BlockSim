import random
import itertools
import numpy as np
import operator
from InputsConfig import InputsConfig as p
from Statistics import Statistics
from Models.Network import Network


class Transaction(object):

    """ Defines the Ethereum Block model.

    :param int id: the uinque id or the hash of the transaction
    :param int timestamp: the time when the transaction is created. In case of Full technique, this will be array of two value (transaction creation time and receiving time)
    :param int sender: the id of the node that created and sent the transaction
    :param int to: the id of the recipint node
    :param int value: the amount of cryptocurrencies to be sent to the recipint node
    :param int size: the transaction size in MB
    :param float fee: the fee of the transaction
    :param int security_level: the security level of the transaction
    """

    def __init__(self,
                 id=0,
                 timestamp=0 or [],
                 sender=0,
                 to=0,
                 value=0,
                 size=0.000546,
                 fee=0,
                 security_level=0):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to = to
        self.value = value
        self.size = size
        self.fee = fee
        self.security_level = security_level


class LightTransaction():

    pending_transactions = []  # shared pool of pending transactions

    def create_transactions():

        LightTransaction.pending_transactions = []
        pool = LightTransaction.pending_transactions
        Psize = int(p.Tn * p.Binterval)

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx = Transaction()

            tx.id = random.randrange(100000000000)
            tx.sender = random.choice(p.NODES).id
            tx.to = random.choice(p.NODES).id
            tx.size = random.expovariate(1/p.Tsize)
            tx.fee = random.expovariate(1/p.Tfee)

            pool += [tx]

        random.shuffle(pool)

    ##### Select and execute a number of transactions to be added in the next block #####

    def execute_transactions():
        transactions = []  # prepare a list of transactions to be included in the block
        size = 0  # calculate the total block gaslimit
        count = 0
        blocksize = p.Bsize
        pool = LightTransaction.pending_transactions

        # sort pending transactions in the pool based on the gasPrice value
        pool = sorted(pool, key=lambda x: x.fee, reverse=True)

        while count < len(pool):
            if (blocksize >= pool[count].size):
                blocksize -= pool[count].size
                transactions += [pool[count]]
                size += pool[count].size
            count += 1

        return transactions, size


class FullTransaction():

    def create_transactions():
        total_tx_count = int(p.Tn * p.simTime)
        security_level_rand_pool = list(itertools.chain(*[
            [-security_level for _ in range(int(float(weight)*100))] for security_level, weight in enumerate(p.TProbability)
        ]))

        for i in range(total_tx_count):
            sender = random.choice(p.NODES)
            creation_time = receive_time = random.randint(0, p.simTime-1)
            security_level = random.choice(security_level_rand_pool)
            fee = random.expovariate(1/(p.Tfee * (2**security_level)))

            tx = Transaction(
                id=random.randrange(100000000000),
                timestamp=[creation_time, receive_time],
                sender=sender.id,
                to=random.choice(p.NODES).id,
                size=random.expovariate(1/p.Tsize),
                security_level=security_level,
                fee=fee,
            )

            sender.transactionsPool.append(tx)
            FullTransaction.transaction_prop(tx)

        # sort transactions by fee asc
        for node in p.NODES:
            node.transactionsPool.sort(
                key=operator.attrgetter('fee'), reverse=True)

    # Transaction propogation & preparing pending lists for miners
    def transaction_prop(tx):
        # Fill each pending list. This is for transaction propogation
        for node in p.NODES:
            if tx.sender != node.id:
                # transaction propogation delay in seconds
                tx.timestamp[1] = tx.timestamp[1] + Network.tx_prop_delay()
                node.transactionsPool.append(tx)

    def execute_transactions(miner, block):
        block_security_level = block.security_level()

        transactions = []  # prepare a list of transactions to be included in the block
        size = 0  # calculate the total block gaslimit

        for idx, tx in enumerate(miner.transactionsPool):
            # move out timeout tx from transactionsPool
            if block.timestamp > tx.timestamp[0] + p.Ttimeout:
                Statistics.tx_timeout_count[-tx.security_level] += 1
                del miner.transactionsPool[idx]
                continue

            if p.Bsize - size >= tx.size and block.timestamp >= tx.timestamp[1] and block_security_level >= tx.security_level:
                transactions.append(tx)
                size += tx.size

        return transactions, size
