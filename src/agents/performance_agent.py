from maspy import Agent, Goal, gain, pl


class PerformanceAgent(Agent):

    def __init__(self, agent_name=None):
        super().__init__(agent_name)
        self.add(Goal("low_performance"))
        self.add(Goal("high_performance"))

    @pl(gain, Goal("low_performance"))
    def notify_low_performance(self, src):
        self.notify_performance_status({"player": "Lionel Messi", "status": "high"})

    @pl(gain, Goal("high_performance"))
    def notify_high_performance(self, src):
        self.notify_performance_status({"player": "Neymar", "status": "low"})
