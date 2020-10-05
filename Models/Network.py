import random
from InputsConfig import InputsConfig as p


class Network:

    # Delay for propagating blocks in the network
    def block_prop_delay():
        if p.Bdelay == 0:
            return 0
        return random.expovariate(1/p.Bdelay)

    # Delay for propagating transactions in the network
    def tx_prop_delay():
        if p.Tdelay == 0:
            return 0
        return random.expovariate(1/p.Tdelay)
