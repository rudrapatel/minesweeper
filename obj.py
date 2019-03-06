class mine:
    def __init__(self, node, blown):
        self.node = node
        self.blown = blown # true if agent stepped on the mine


class inferenceProbability:
    def __init__(self, probability, numNeighbor):
        # self.node = node
        self.p = probability
        self.numNeighbor = numNeighbor
