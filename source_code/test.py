import pytest
import Agent
# from Agent import agent_distance
# Python File to test class functions 

agent1 = Agent.Agent(0,0)
agent2 = Agent.Agent(1, 0)
agent3 = Agent.Agent(2, 1)

def test_agent_distance():
    THRESHOLD = 10000 # can change
    contacts = Agent.Agent.agent_distance(agent1, agent2, 1, 10000)
    print(agent1.contacts.items())
    assert(len(agent1.contacts[1])) == 1
    assert(len(agent2.contacts[1])) == 1

if __name__ == "__main__": 
    test_agent_distance()
    
