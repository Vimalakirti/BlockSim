from InputsConfig import InputsConfig as p
import random
from Models.Block import Block
from Event import Event, Queue

if p.model == 2:
    from Models.Ethereum.Block import Block
elif p.model == 3:
    from Models.Bplusplus.Block import Block
else:
    from Models.Block import Block


class Scheduler:

    # Schedule a block creation event for a miner and add it to the event list
    def create_block_event(miner, eventTime):
        eventType = "create_block"
        if eventTime <= p.simTime:
            # prepare attributes for the event
            block = Block()
            block.miner = miner.id
            block.id = random.randrange(100000000000)
            block.timestamp = eventTime
            if p.model == 3:
                virtual_block = miner.next_unfinished_virtual_block()
                block.depth = virtual_block.depth
                block.branch_id = virtual_block.next_branch_id()
            else:
                block.depth = len(miner.blockchain)
                block.previous = miner.last_block().id

            event = Event(eventType, block.miner, eventTime,
                          block)  # create the event
            Queue.add_event(event)  # add the event to the queue

    # Schedule a block receiving event for a node and add it to the event list
    def receive_block_event(recipient, block, blockDelay):
        receive_block_time = block.timestamp + blockDelay
        if receive_block_time <= p.simTime:
            e = Event("receive_block", recipient.id, receive_block_time, block)
            Queue.add_event(e)
