import random
import numpy as np
import operator
from InputsConfig import InputsConfig as p
from Statistics import Statistics
from Models.Network import Network
from Models.Ethereum.Distribution.DistFit import DistFit

class Transaction(object):

    """ Defines the Ethereum Block model.

    :param int id: the uinque id or the hash of the transaction
    :param int timestamp: the time when the transaction is created. In case of Full technique, this will be array of two value (transaction creation time and receiving time)
    :param int sender: the id of the node that created and sent the transaction
    :param int to: the id of the recipint node
    :param int value: the amount of cryptocurrencies to be sent to the recipint node
    :param int size: the transaction size in MB
    :param int gasLimit: the maximum amount of gas units the transaction can use. It is specified by the submitter of the transaction
    :param int usedGas: the amount of gas used by the transaction after its execution on the EVM
    :param int gasPrice: the amount of cryptocurrencies (in Gwei) the submitter of the transaction is willing to pay per gas unit
    :param float fee: the fee of the transaction (usedGas * gasPrice)
    """

    def __init__(self,
	 id=0,
	 timestamp=0 or [],
	 sender=0,
         to=0,
         value=0,
	 size=0.000546,
         gasLimit= 8000000,
         usedGas=0,
         gasPrice=0,
         fee=0):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to= to
        self.value=value
        self.size = size
        self.gasLimit=gasLimit
        self.usedGas = usedGas
        self.gasPrice=gasPrice
        self.fee= usedGas * gasPrice



class LightTransaction():

    pending_transactions=[] # shared pool of pending transactions
    #x=0 # counter to only fit distributions once during the simulation

    def create_transactions():

        LightTransaction.pending_transactions=[]
        pool= LightTransaction.pending_transactions
        Psize= int(p.Tn * p.Binterval)
        
        #if LightTransaction.x<1:
        DistFit.fit() # fit distributions
        gasLimit,usedGas,gasPrice,_ = DistFit.sample_transactions(Psize) # sampling gas based attributes for transactions from specific distribution

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            tx.sender = random.choice (p.NODES).id
            tx.to= random.choice (p.NODES).id
            tx.gasLimit=gasLimit[i]
            tx.usedGas=usedGas[i]
            tx.gasPrice=gasPrice[i]/1000000000
            tx.fee= tx.usedGas * tx.gasPrice

            pool += [tx]


        random.shuffle(pool)


    ##### Select and execute a number of transactions to be added in the next block #####
    def execute_transactions():
        sorted_tx_pool = sorted(LightTransaction.pending_transactions,
                      key=lambda x: x.gasPrice, reverse=True)

        transactions = []  # prepare a list of transactions to be included in the block
        used_gas = 0  # calculate the total block gaslimit

        for tx in sorted_tx_pool:
            if p.Blimit - used_gas >= tx.gasLimit:
                transactions.append(tx)
                used_gas += tx.usedGas

        return transactions, used_gas

class FullTransaction():

    def create_transactions():
        Psize= int(p.Tn * p.simTime)

        DistFit.fit() # fit distributions
        gasLimit,usedGas,gasPrice,_ = DistFit.sample_transactions(Psize) # sampling gas based attributes for transactions from specific distribution

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            creation_time= random.randint(0,p.simTime-1)
            receive_time= creation_time
            tx.timestamp= [creation_time,receive_time]
            sender= random.choice (p.NODES)
            tx.sender = sender.id
            tx.to= random.choice (p.NODES).id
            tx.gasLimit=gasLimit[i]
            tx.usedGas=usedGas[i]
            tx.gasPrice=gasPrice[i]/1000000000
            tx.fee= tx.usedGas * tx.gasPrice
            
            sender.transactionsPool.append(tx)
            FullTransaction.transaction_prop(tx)

        # sort transactions by fee asc
        for node in p.NODES:
            node.transactionsPool.sort(
                key=operator.attrgetter('gasPrice'), reverse=True)

    # Transaction propogation & preparing pending lists for miners
    def transaction_prop(tx):
        # Fill each pending list. This is for transaction propogation
        for node in p.NODES:
            if tx.sender != node.id:
                # transaction propogation delay in seconds
                tx.timestamp[1] = tx.timestamp[1] + Network.tx_prop_delay()
                node.transactionsPool.append(tx)

    def execute_transactions(miner,currentTime):
        transactions= [] # prepare a list of transactions to be included in the block
        used_gas = 0 # calculate the total block gaslimit

        for idx, tx in enumerate(miner.transactionsPool):
            # move out timeout tx from transactionsPool
            if currentTime > tx.timestamp[0] + p.Ttimeout:
                Statistics.tx_timeout_count += 1
                del miner.transactionsPool[idx]
                continue

            if (p.Blimit - used_gas >= tx.gasLimit and currentTime >= tx.timestamp[1]):
                transactions.append(tx)
                used_gas += tx.usedGas

        return transactions, used_gas
