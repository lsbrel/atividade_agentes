from maspy import Environment, Percept


class FotballField(Environment):

    def notify_injury(self, agent, player):
        self.print(f"Injury announced by: {agent}, player: {player}")
        self.create(Percept("injury", {"agent": agent, "player": player}))

    def notify_performance_status(self, agent, performance):
        self.print(
            f"Performance status announced by: {agent}, performance_status: {performance}"
        )

    def notify_tiredness(self, agent, player):
        self.print(
            f"Tiredness status announced by: {agent}, performance_status: {player}"
        )
