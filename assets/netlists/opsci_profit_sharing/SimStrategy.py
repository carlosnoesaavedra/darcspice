import math
from enforce_typing import enforce_types

from engine import SimStrategyBase
from util.constants import S_PER_HOUR

@enforce_types
class SimStrategy(SimStrategyBase.SimStrategyBase):
    def __init__(self):
        #===initialize self.time_step, max_ticks====
        super().__init__()

        #===set base-class values we want for this netlist====
        self.setTimeStep(S_PER_HOUR)
        self.setMaxTime(10, 'years') #typical runs: 10 years, 20 years, 150 years

        #===new attributes specific to this netlist===
        self.TICKS_BETWEEN_PROPOSALS = 6480
        self.PRICE_OF_ASSETS = 1000 # OCEAN
        self.RATIO_FUNDS_TO_PUBLISH = 0.4 # 40% of grant funding will go towards "doing work" & publishing
        '''
        Some additional parameters that will enable more experimentation (not currently in use)
        '''
        self.FUNDING_TIME_DEPENDENCE = True # meaning that TICKS_BETWEEN_PROPOSALS should be used
        self.MAX_PROPOSALS_FUNDED_AT_A_TIME = 1 # this would be used if FUNDING_TIME_DEPENDENCE = False, <=> funding as projects finish
        self.PROPOSAL_SETUP = {'grant_requested': 1000, # can be used as a parameter in ResearcherAgent in SimState
                               'assets_generated': 1,
                               'no_researchers': 10}

        # DT parameters
        self.DT_init = 100.0

        # DATA TOKEN COMPATIBILITY WIP
        # # pool
        # self.DT_stake = 20.0
        # self.pool_weight_DT    = 3.0
        # self.pool_weight_OCEAN = 7.0
        # assert (self.pool_weight_DT + self.pool_weight_OCEAN) == 10.0