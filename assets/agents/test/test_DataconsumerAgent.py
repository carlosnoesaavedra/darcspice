import pytest

from assets.agents.PoolAgent import PoolAgent
from assets.agents.DataconsumerAgent import DataconsumerAgent
from assets.agents.PublisherAgent import PublisherAgent
from engine.AgentBase import AgentBase
from engine.AgentDict import AgentDict
from util.constants import S_PER_HOUR

class MockSS:
    def __init__(self):
        #seconds per tick
        self.time_step: int = S_PER_HOUR
        self.pool_weight_DT: float = 1.0
        self.pool_weight_OCEAN: float = 1.0

class MockState:
    def __init__(self):
        self.agents = AgentDict({})
        self.ss = MockSS()
    def addAgent(self, agent):
        self.agents[agent.name] = agent

class MockAgent(AgentBase):
    def takeStep(self, state):
        pass

# @pytest.mark.skip(reason="TODO FIXME")
def test_doBuyAndConsumeDT(alice_pool):
    state = MockState()

    agent = DataconsumerAgent("agent1",USD=0.0,OCEAN=1000.0)

    assert agent._s_since_buy == 0
    assert agent._s_between_buys > 0

    assert not agent._doBuyAndConsumeDT(state)

    agent._s_since_buy += agent._s_between_buys
    assert not state.agents.filterToPool().values()
    assert not agent._doBuyAndConsumeDT(state) #still no, since no pools

    state.agents["pool1"] = PoolAgent("pool1", alice_pool)
    assert state.agents.filterToPool().values() #have pools
    assert agent._candPoolAgents(state) #have useful pools
    assert agent._doBuyAndConsumeDT(state)

def test_buyDT(alice_info):
    state = MockState()
    alice_agent = MockAgent("agent1", USD=0.0, OCEAN=0.0)
    alice_agent._wallet = alice_info.agent_wallet
    state.addAgent(alice_agent)
    agent = DataconsumerAgent("con1", USD=0.0, OCEAN=1000.0) 
    state.addAgent(agent)

    alice_pool = alice_info.pool

    agent._s_since_buy += agent._s_between_buys

    state.agents["pool1"] = PoolAgent("pool1", alice_pool)

    assert state.agents.filterToPool().values() #have pools
    assert agent._candPoolAgents(state) #have useful pools
    assert agent._doBuyAndConsumeDT(state)

    # buyDT
    dt = state.agents["pool1"].datatoken
    assert agent.OCEAN() == 1000.0
    assert agent.DT(dt) == 0.0
    pool_agent, OCEAN_spend = agent._buyDT(state)
    assert agent.OCEAN() == 1000.0 - OCEAN_spend
    assert agent.DT(dt) == 1.0

    # consumeDT
    assert state.agents.agentByAddress(pool_agent.controller_address)

    # we model lag from consume to value creation simply by a delay between buys
    assert alice_agent.DT(dt) == 80.0
    agent._consumeDT(state, pool_agent, OCEAN_spend)
    assert agent.OCEAN() == 1000.0 + OCEAN_spend * agent.profit_margin_on_consume
    assert agent.DT(dt) == 0.0
    assert alice_agent.DT(dt) == 81.0
