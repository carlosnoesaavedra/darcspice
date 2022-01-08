from enforce_typing import enforce_types
import random

from engine import AgentBase
from util import constants
                    
@enforce_types
class SimpleStakerspeculatorAgent(AgentBase.AgentBaseNoEvm):
    """Speculates by staking and unstaking | No pools/DTs/EVM"""
    
    def __init__(self, name: str, USD: float, OCEAN: float):
        super().__init__(name, USD, OCEAN)

        self._s_since_speculate = 0
        self._s_between_speculates = 8 * constants.S_PER_HOUR #magic number
        
    def takeStep(self, state):
        # the agent's wallet is automatically assumed to be "staked", so the staker only collects fees
        # which are immediately restaked
        pass

    def _doSpeculateAction(self, state):
        pool_agents = state.agents.filterToPool().values()
        if not pool_agents:
            return False
        else:
            return self._s_since_speculate >= self._s_between_speculates

    def _speculateAction(self, state):
        pool_agents = state.agents.filterToPool().values()
        assert pool_agents, "need pools to be able to speculate"
        
        pool = random.choice(list(pool_agents)).pool
        # BPT = self.BPT(pool)

        # if BPT > 0.0 and random.random() < 0.50: #magic number
        #     BPT_sell = 0.10 * BPT #magic number
        #     self.unstakeOCEAN(BPT_sell, pool)
            
        # else:
        #     OCEAN_stake = 0.10 * self.OCEAN() #magic number

        # In this model, staker always stakes everything to get more rewards
        OCEAN_stake = self.OCEAN()
        self.stakeOCEAN(OCEAN_stake, pool)
        
            
