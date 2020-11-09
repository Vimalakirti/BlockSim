# B++ Simulation

## B++ Simulation
The simulator of **B++** is implemented in this repository. This simulation is based on **BlockSim**.
(B++ is still under review currently.)

## What is BlockSim Simulator?
**BlockSim** is an open source blockchain simulator, capturing network, consensus and incentives layers of blockchain systems. For more details about BlockSim, we refer to our journal paper that can be freely accessed online https://www.frontiersin.org/articles/10.3389/fbloc.2020.00028/full

## Installation and Requirements

Before you use the simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- `requirements.txt` 
> pip3 install -r requirements.txt

## Running the simulator

Before you run the simulator, you can access the configuration file `InputsConfig.py` to choose the model of interest (Base Model 0, Bitcoin Model 1, Ethereum Model 2 and B++ Model 3) and to set up the related parameters.
The parameters include the number of nodes (and their fraction of hash power), the block interval time, the block propagation delays, the block and transaction sizes, the block rewards, the tranaction fees etc. On top of that, the minimal security level of B++ can also be set. Each model has a slightly different (or additional) parameters to capture it.

To run the simulator, one needs to trigger the main class `Main.py` either from the command line
> python3 Main.py

Or you may use our scripts (which are located in `./script`) to run experiments, the environmental parameters are put in `.env.base`, `.env.bitcoin`, `.env.ethereum` and `.env.b++`:
- Run Ethereum
    > bash script/run.sh ethereum run
- Run Bitcoin
    > bash script/run.sh bitcoin run
- Run B++
    1. Try different minimal security level in B++:
    > bash script/run.sh b++ run_different_dmin
    2. The minimal security level is zero:
    > bash script/run.sh b++ run_as_bitcoin
    3. Try different miner number:
    > bash script/run.sh b++ run_different_node_count

## Statistics and Results

The results of the simulator is printed in an excel file at the end of the simulation. The results include the blockchain ledger, number of blocks mined, number of stale (uncles) blocks and the rewards gained by each miner etc. 
