import numpy as np
from scipy.stats import expon
import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as StatCls
import numpy
from numpy.random import choice
import ConditionTypeProbs as C_P
import DT_Condition_1 as DT
import DT_Condition_2 as DT_C2

probs = numpy.random.dirichlet(alpha=(1, 2), size=None)
conditions_list = ['a', 'b']

draw = choice(a=conditions_list, p=probs)

class Patient:
    def __init__(self, id):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(self._id)
        self._cost_utility = []
        self._OS_cost = 0
        self._NoOS_cost = 0
        self._OS_utility = 0
        self._NoOS_utility = 0
        self._DALY = 0

    def simulate (self):

        if draw == 'a':
            import InputData_Condition1 as D
            tree_OS=DT.DT.DecisionNode('d1', dict_decisions=DT.dictDecisions_OS,
                                       cum_prob=1, dict_chances=DT.dictChances_OS, dict_terminals=DT.dictTerminal_OS)

            self._cost_utility=tree_OS.get_cost_utility()
            self._OS_cost=tree_OS.get_OS_cost()
            self._OS_utility=tree_OS.get_OS_utility()
            tree_NoOS = DT.DT.DecisionNode('d2', dict_decisions=DT.dictDecisions_NoOS, cum_prob=1,
                                              dict_chances=DT.dictChances_NoOS, dict_terminals=DT.dictTerminal_NoOS)
            self._cost_utility=tree_NoOS.get_cost_utility()
            self._NoOS_cost=tree_NoOS.get_NoOS_cost()
            self._NoOS_utility=tree_NoOS.get_NoOS_utility()
            self._DALY = DT.get_DALY(self)
        if draw == 'b':
            tree_OS = DT.DT.DecisionNode('d1', dict_decisions=DT.dictDecisions_OS,
                                            cum_prob=1, dict_chances=DT.dictChances_OS,
                                            dict_terminals=DT.dictTerminal_OS)

            self._cost_utility = tree_OS.get_cost_utility()
            self._OS_cost = tree_OS.get_OS_cost()
            self._OS_utility = tree_OS.get_OS_utility()
            tree_NoOS = DT.DT.DecisionNode('d2', dict_decisions=DT.dictDecisions_NoOS, cum_prob=1,
                                              dict_chances=DT.dictChances_NoOS,
                                              dict_terminals=DT.dictTerminal_NoOS)
            self._cost_utility = tree_NoOS.get_cost_utility()
            self._NoOS_cost = tree_NoOS.get_NoOS_cost()
            self._NoOS_utility = tree_NoOS.get_NoOS_utility()
            self._DALY = DT.get_DALY(self)

    def get_DALY(self):
        return self._DALY

    def get_cost_utility(self):
        return self._cost_utility

    def get_OS_cost(self):
        return self._OS_cost

    def get_NoOS_cost(self):
        return self._NoOS_cost

    def get_OS_utility(self):
        return self._OS_utility

    def get_NoOS_utility(self):
        return self._NoOS_utility

class YearofPatients:
    def __init__(self, id):
        self._patients = []
        # eventually we'll want to add other metrics here. Like how many died, etc.

        self._initial_pop_size=100
        # fixed internally because we're going to make this number random eventually.
        # Maybe we'll change this later, but this should work for now.

        for i in range(self._initial_pop_size):
            # create a new patient (use id * pop_size + i as patient id)
            patient = Patient(id * self._initial_pop_size + i)
            self._patients.append(patient)

    def simulate(self):
        """ simulate the cohort of patients over the specified number of time-steps
        :returns outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            patient.simulate()

        # return the cohort outputs
        return YearofPatientsOutputs(self)

    def get_number_of_patients(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients


class YearofPatientsOutputs:
    def __init__(self, simulated_cohort):
        """ extracts outputs from a simulated cohort
        :param simulated_cohort: a cohort after being simulated
        """

        #self._costs_utilities = []
        self._OS_costs = []
        self._NoOS_costs = []
        self._OS_utilities = []
        self._NoOS_utilities = []
        self._DALY = []

        # find patients' survival times
        for patient in simulated_cohort.get_patients():

            # cost and utility
            #self._costs_utilities.append(patient.get_cost_utility())
            self._OS_costs.append(patient.get_OS_cost())
            self._NoOS_costs.append(patient.get_NoOS_cost())
            self._OS_utilities.append(patient.get_OS_utility())
            self._NoOS_utilities.append(patient.get_NoOS_utility())
            self._DALY.append(patient.get_DALY())

        # summary statistics
        self._sumStat_OS_cost = StatCls.SummaryStat('Expected Op Smile Cost', self._OS_costs)
        self._sumStat_NoOS_cost = StatCls.SummaryStat('Expected No Op Smile Cost', self._NoOS_costs)
        self._sumStat_OS_utility = StatCls.SummaryStat('Expected Op Smile utility', self._OS_utilities)
        self._sumStat_NoOS_utility = StatCls.SummaryStat('Expected No Op Smile utility', self._NoOS_utilities)
        self._sumStat_DALY = StatCls.SummaryStat('DALY', self._DALY)


  #  def get_costs_utilities(self):
   #     return self._costs_utilities

    def get_DALY(self):
        return self._DALY

    def get_OS_costs(self):
        return self._OS_costs

    def get_NoOS_costs(self):
        return self._NoOS_costs

    def get_OS_utilities(self):
        return self._OS_utilities

    def get_NoOS_utilities(self):
        return self._NoOS_utilities

    def get_sumStat_OS_cost(self):
        return self._sumStat_OS_cost

    def get_sumStat_NoOS_cost(self):
        return self._sumStat_NoOS_cost

    def get_sumStat_OS_utility(self):
        return self._sumStat_OS_utility

    def get_sumStat_NoOS_utility(self):
        return self._sumStat_NoOS_utility

    def get_sumStat_DALY(self):
        return self._sumStat_DALY