#!/bin/python3.14
from agents.injury_agent import InjuryAgent
from agents.performance_agent import PerformanceAgent
from agents.tiredness_agent import TirednessAgent
from environments.fotball_field import FotballField
from maspy import Admin


def main():

    environment = FotballField()

    injury_agent = InjuryAgent(agent_name="Injury Agent")
    performance_agent = PerformanceAgent(agent_name="Performance Agent")
    tiredness_agent = TirednessAgent(agent_name="Tiredness Agent")

    Admin().connect_to(
        agents=[injury_agent, performance_agent, tiredness_agent], targets=environment
    )
    Admin().start_system()


if __name__ == "__main__":
    main()
