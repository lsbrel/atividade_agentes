from maspy import Agent, Goal, gain, pl


class TirednessAgent(Agent):

    def __init__(self, agent_name=None):
        super().__init__(agent_name)
        self.add(Goal("tiredness"))

    @pl(gain, Goal("tiredness"))
    def notify(self, src):
        self.notify_tiredness({"player": "Marquinhos"})
