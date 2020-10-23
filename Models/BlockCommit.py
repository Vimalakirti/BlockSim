from InputsConfig import InputsConfig as p


class BlockCommit:
    # Handling and running Events
    def handle_event(event):
        if event.type == "create_block":
            BlockCommit.generate_block(event)
        elif event.type == "receive_block":
            BlockCommit.receive_block(event)

    # Block Creation Event
    def generate_block(event):
        pass

    # Block Receiving Event
    def receive_block(event):
        pass

    # Select a new miner to build a new block
    def generate_next_block(node, currentTime):
        pass
    # Generate initial blocks to start the simulation with

    def generate_initial_events():
        pass
    # Propagate the genrated block to other nodes in the network

    def propagate_block(block):
        pass
    # Update local blockchain, if necessary, upon receiving a new valid block

    def update_local_blockchain(node, miner, depth):
        # the node here is the one that needs to update its blockchain, while miner here is the one who owns the last block generated
        # the node will update its blockchain to mach the miner's blockchain
        i = 0
        while (i < depth):
            if (i < len(node.blockchain)):
                # and (self.node.blockchain[i-1].id == Miner.blockchain[i].previous) and (i>=1):
                if (node.blockchain[i].id != miner.blockchain[i].id):
                    #node.unclechain.append(node.blockchain[i]) # move block to unclechain
                    newBlock = miner.blockchain[i]
                    if p.hasTrans and p.Ttechnique == "Full":
                        BlockCommit.unset_mined_txs(
                            node, node.blockchain[i].transactions)
                        BlockCommit.set_mined_txs(node, newBlock.transactions)
                    node.blockchain[i] = newBlock
            else:
                newBlock = miner.blockchain[i]
                node.blockchain.append(newBlock)
                if p.hasTrans and p.Ttechnique == "Full":
                    BlockCommit.set_mined_txs(node, newBlock.transactions)
            i += 1

    def set_mined_txs(node, txs):
        node.mined_tx_set = node.mined_tx_set.union(set([tx.id for tx in txs]))

    def unset_mined_txs(node, txs):
        node.mined_tx_set = node.mined_tx_set - set([tx.id for tx in txs])
