import random
import itertools
import numpy as np
import operator
from heapq import merge
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

    def __lt__(self, other):
        return self.fee < other.fee

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
        sorted_tx_pool = sorted(LightTransaction.pending_transactions,
                                key=lambda x: x.fee, reverse=True)

        transactions = []
        size = 0

        for tx in sorted_tx_pool:
            if p.Bsize - size >= tx.size:
                transactions.append(tx)
                size += tx.size

        return transactions, size


class FullTransaction():
    tx_set = {}

    def create_transactions():
        FullTransaction.tx_set = {}
        total_tx_count = int(p.Tn * p.simTime)
        security_level_rand_pool = list(itertools.chain(*[
            [-security_level for _ in range(int(float(weight)*100))] for security_level, weight in enumerate(p.TProbability)
        ]))

        while len(FullTransaction.tx_set) < total_tx_count:
            id = random.randrange(100000000000000)
            if id in FullTransaction.tx_set:
                continue

            sender = random.choice(p.NODES)
            creation_time = receive_time = random.randint(0, p.simTime-1)
            security_level = random.choice(security_level_rand_pool)
            fee = random.expovariate(1/(p.Tfee * (2**security_level)))

            tx = Transaction(
                id=id,
                timestamp=[creation_time, receive_time],
                sender=sender.id,
                to=random.choice(p.NODES).id,
                size=random.expovariate(1/p.Tsize),
                security_level=security_level,
                fee=fee,
            )

            sender.all_transactions.append(tx)
            FullTransaction.transaction_prop(tx)

            FullTransaction.tx_set[tx.id] = tx

        # sort transactions by fee asc
        for node in p.NODES:
            node.all_transactions.sort(key=lambda tx: tx.timestamp[1])

    # Transaction propogation & preparing pending lists for miners
    def transaction_prop(tx):
        # Fill each pending list. This is for transaction propogation
        for node in p.NODES:
            if tx.sender != node.id:
                # transaction propogation delay in seconds
                tx.timestamp[1] = tx.timestamp[1] + Network.tx_prop_delay()
                node.all_transactions.append(tx)

    def update_tx_pool(miner, block):
        valid_tx_idx = 0
        for idx, tx in enumerate(miner.all_transactions):
            if tx.timestamp[1] > block.timestamp:
                valid_tx_idx = idx
                break

        new_txs = sorted(miner.all_transactions[:valid_tx_idx], reverse=True)
        del miner.all_transactions[:valid_tx_idx]

        block_security_level = block.security_level()
        miner.transactionsPool = [tx for tx in list(merge(
            miner.transactionsPool, new_txs, reverse=True)) if tx.id not in miner.mined_tx_set and block.timestamp < tx.timestamp[0] + p.Ttimeout and block_security_level >= tx.security_level]

    def execute_transactions(miner, block):
        FullTransaction.update_tx_pool(miner, block)

        transactions = []
        size = 0

        for tx in miner.transactionsPool:
            if p.Bsize - size >= tx.size:
                transactions.append(tx)
                size += tx.size

        return transactions, size
