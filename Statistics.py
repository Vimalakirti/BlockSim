import pandas as pd
import numpy as np
from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c
from Models.Incentives import Incentives


class Statistics:

    ########################################################### Global variables used to calculate and print simuation results ###########################################################################################
    totalBlocks = 0
    mainBlocks = 0
    totalUncles = 0
    uncleBlocks = 0
    staleBlocks = 0
    uncleRate = 0
    staleRate = 0
    blockData = []
    tx_timeout_count = 0
    if p.model == 3:
        tx_timeout_count = [0] * (1-p.Bdmin)
    blocksResults = []
    tx_latency_mean_results = []
    tx_timeout_count_results = []
    # rows number of miners * number of runs, columns =7
    profits = [[0 for x in range(7)] for y in range(p.Runs * len(p.NODES))]
    index = 0
    chain = []

    def calculate():
        Statistics.global_chain()  # print the global chain
        # calcuate and print block statistics e.g., # of accepted blocks and stale rate etc
        Statistics.blocks_results()
        # calculate and distribute the revenue or reward for miners
        Statistics.profit_results()
        # calculate tx latency
        if p.Ttechnique == 'Full':
            Statistics.transaction_latency_result()

    ########################################################### Calculate block statistics Results ###########################################################################################
    def blocks_results():
        trans = 0

        Statistics.mainBlocks = len(c.global_chain)-1
        if p.model == 3:
            full_cycle_block_count = \
                (Statistics.mainBlocks // (1-p.Bdmin)) * (2**(1-p.Bdmin)-1)
            leftover_block_count = sum(
                [2**(abs(p.Bdmin) - i) for i in range(Statistics.mainBlocks % (1-p.Bdmin))])
            Statistics.staleBlocks = Statistics.totalBlocks - \
                full_cycle_block_count - leftover_block_count
        else:
            Statistics.staleBlocks = Statistics.totalBlocks - Statistics.mainBlocks
        for b in c.global_chain:
            if p.model == 2:
                Statistics.uncleBlocks += len(b.uncles)
            else:
                Statistics.uncleBlocks = 0
            trans += len(b.transactions)
        Statistics.staleRate = round(
            Statistics.staleBlocks/Statistics.totalBlocks * 100, 2)
        if p.model == 2:
            Statistics.uncleRate = round(
                Statistics.uncleBlocks/Statistics.totalBlocks * 100, 2)
        else:
            Statistics.uncleRate == 0
        Statistics.blockData = [Statistics.totalBlocks, Statistics.mainBlocks,  Statistics.uncleBlocks,
                                Statistics.uncleRate, Statistics.staleBlocks, Statistics.staleRate, trans]
        Statistics.blocksResults += [Statistics.blockData]

    def transaction_latency_result():
        if p.model == 3:
            tx_latencies = [[] for _ in range(1-p.Bdmin)]

            # calculate global chain tx latency of each dmin
            for block in c.global_chain:
                for branch in block.branches:
                    for tx in branch.transactions:
                        idx = -tx.security_level
                        tx_latencies[idx].append(
                            branch.timestamp - tx.timestamp[0])

            last_block_timestamp = max([branch.timestamp for branch in c.global_chain[-1].branches])
            # calculate tx not mined timout count of each dmin
            for node in p.NODES:
                for tx in node.transactionsPool:
                    if last_block_timestamp > tx.timestamp[0] + p.Ttimeout:
                        Statistics.tx_timeout_count[-tx.security_level] += 1

            Statistics.tx_latency_mean_results.append(
                [np.mean(l) for l in tx_latencies])
            Statistics.tx_timeout_count_results.append(
                Statistics.tx_timeout_count)
        else:
            tx_latencies = []

            # calculate global chain tx latency
            for block in c.global_chain:
                for tx in block.transactions:
                    tx_latencies.append(block.timestamp - tx.timestamp[0])
                    
            last_block_timestamp = c.global_chain[-1].timestamp
            for node in p.NODES:
                for tx in node.transactionsPool:
                    if last_block_timestamp > tx.timestamp[0] + p.Ttimeout:
                        Statistics.tx_timeout_count += 1

            Statistics.tx_latency_mean_results.append(np.mean(tx_latencies))
            Statistics.tx_timeout_count_results.append(
                Statistics.tx_timeout_count)
    ########################################################### Calculate and distibute rewards among the miners ###########################################################################################
    def profit_results():

        for m in p.NODES:
            i = Statistics.index + m.id * p.Runs
            Statistics.profits[i][0] = m.id
            if p.model == 0:
                Statistics.profits[i][1] = "NA"
            else:
                Statistics.profits[i][1] = m.hashPower
            Statistics.profits[i][2] = m.blocks
            if p.model == 3:
                Statistics.profits[i][3] = round(
                    m.blocks/Statistics.totalBlocks * 100, 2)
            else:
                Statistics.profits[i][3] = round(
                    m.blocks/Statistics.mainBlocks * 100, 2)
            if p.model == 2:
                Statistics.profits[i][4] = m.uncles
                Statistics.profits[i][5] = round(
                    (m.blocks + m.uncles)/(Statistics.mainBlocks + Statistics.totalUncles) * 100, 2)
            else:
                Statistics.profits[i][4] = 0
                Statistics.profits[i][5] = 0
            Statistics.profits[i][6] = m.balance

        Statistics.index += 1

    ########################################################### prepare the global chain  ###########################################################################################
    def global_chain():
        if p.model == 0 or p.model == 1 or p.model == 3:
            for i in c.global_chain:
                block = [i.depth, i.id, i.previous, i.timestamp,
                         i.miner, len(i.transactions), i.size]
                Statistics.chain += [block]
        elif p.model == 2:
            for i in c.global_chain:
                block = [i.depth, i.id, i.previous, i.timestamp,
                         i.miner, len(i.transactions), i.usedgas, len(i.uncles)]
                Statistics.chain += [block]

    ########################################################### Print simulation results to Excel ###########################################################################################
    def print_to_excel(fname):

        df1 = pd.DataFrame({'Block Time': [p.Binterval], 'Block Propagation Delay': [
                           p.Bdelay], 'No. Miners': [len(p.NODES)], 'Simulation Time': [p.simTime]})
        #data = {'Stale Rate': Results.staleRate,'Uncle Rate': Results.uncleRate ,'# Stale Blocks': Results.staleBlocks,'# Total Blocks': Results.totalBlocks, '# Included Blocks': Results.mainBlocks, '# Uncle Blocks': Results.uncleBlocks}

        df2 = pd.DataFrame(Statistics.blocksResults)
        df2.columns = ['Total Blocks', 'Main Blocks', 'Uncle blocks',
                       'Uncle Rate', 'Stale Blocks', 'Stale Rate', '# transactions']

        df3 = pd.DataFrame(Statistics.profits)
        df3.columns = ['Miner ID', '% Hash Power', '# Mined Blocks',
                       '% of main blocks', '# Uncle Blocks', '% of uncles', 'Profit (in ETH)']

        df4 = pd.DataFrame(Statistics.chain)
        #df4.columns= ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions','Block Size']
        if p.model == 2:
            df4.columns = ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp',
                           'Miner ID', '# transactions', 'Block Limit', 'Uncle Blocks']
        else:
            df4.columns = ['Block Depth', 'Block ID', 'Previous Block',
                           'Block Timestamp', 'Miner ID', '# transactions', 'Block Size']

        writer = pd.ExcelWriter(fname, engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='InputConfig')
        df2.to_excel(writer, sheet_name='SimOutput')
        df3.to_excel(writer, sheet_name='Profit')
        df4.to_excel(writer, sheet_name='Chain')

        if p.Ttechnique == 'Full':
            df5 = pd.DataFrame(Statistics.tx_latency_mean_results)
            df6 = pd.DataFrame(Statistics.tx_timeout_count_results)
            if p.model == 3:
                df5.columns = df6.columns = [
                    '%d' % -i for i in range(1-p.Bdmin)]
            else:
                df5.columns = df6.columns = ['0']

            df5.to_excel(writer, sheet_name='Tx Latency Mean')
            df6.to_excel(writer, sheet_name='Tx Timeout Count')

        writer.save()

    ########################################################### Reset all global variables used to calculate the simulation results ###########################################################################################
    def reset():
        Statistics.totalBlocks = 0
        Statistics.totalUncles = 0
        Statistics.mainBlocks = 0
        Statistics.uncleBlocks = 0
        Statistics.staleBlocks = 0
        Statistics.uncleRate = 0
        Statistics.staleRate = 0
        Statistics.blockData = []
        Statistics.tx_timeout_count = 0
        if p.model == 3:
            Statistics.tx_timeout_count = [0] * (1-p.Bdmin)

    def reset2():
        Statistics.blocksResults = []
        # rows number of miners * number of runs, columns =7
        Statistics.profits = [
            [0 for x in range(7)] for y in range(p.Runs * len(p.NODES))]
        Statistics.index = 0
        Statistics.chain = []
