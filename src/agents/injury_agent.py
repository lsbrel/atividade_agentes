from maspy import Agent, Goal, gain, pl


class InjuryAgent(Agent):

    def __init__(self, agent_name=None):
        super().__init__(agent_name)
        self.add(Goal("injury"))

    @pl(gain, Goal("injury"))
    def notify(self, src):
        self.notify_injury({"player": "Lionel Messi"})
