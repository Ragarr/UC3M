from .state import State

class MDP:
    def __init__(self, states: list):
        self.states = states

    def calculate_bellman(self, curr_state: State) -> int:
        """
        Using Bellman's ecuation, it returns the most correct policy for a
        current state. It also updates the prefered action of the state based on the result
        :param curr_state: State of wich we want to know the best action policy
        :return: The V of the state
        """
        min_option = None
        for action in curr_state.actions:
            posible_transition_states = []
            prob_transition_states = []

            for i in action.probabilities:
                if action.probabilities[i] != 0:
                    posible_transition_states.append(i)
                    prob_transition_states.append(action.probabilities[i])

            option = 0
            for i in range(len(posible_transition_states)):
                # We search for the V of the state
                for state in self.states:
                    if state.id == posible_transition_states[i]:
                        v = state.V
                option += v*float(prob_transition_states[i])

            if not min_option:
                min_option = option + action.cost
                curr_state.prefered_action = action
            elif option + action.cost < min_option:
                min_option = option + action.cost
                curr_state.prefered_action = action

        return min_option

    def _update_V(self, iterations: int = None) -> None:
        """
        Updates de V (Expected Value) of each state conforming the self.states list
        :return: None
        """
        NUM_DECIMALS = 10

        if iterations:
            for iter in range(iterations):
                new_Vs = []
                for state in self.states:
                    new_Vs.append(self.calculate_bellman(state))
                for i in range(len(self.states)):
                    if self.states[i].id != str(self.objective):
                        self.states[i].V = new_Vs[i]
        else:
            converge = False
            new_Vs = []
            while not converge:
                old_Vs = new_Vs
                new_Vs = []
                for state in self.states:
                    new_Vs.append(self.calculate_bellman(state))
                for i in range(len(self.states)):
                    if self.states[i].id != str(self.objective):
                        self.states[i].V = new_Vs[i]
                if len(old_Vs) == len(new_Vs):
                    for i in range(len(new_Vs)):
                        if int(new_Vs[i] * (10**NUM_DECIMALS)) == int(old_Vs[i] * (10**NUM_DECIMALS)):
                            converge = True
                        else:
                            converge = False
                            break

    def get_state(self, id: str) -> State:
        """
        Returns the state with the given id
        :param id: id of the state
        :return: State
        """
        for state in self.states:
            if float(state.id) == float(id):
                return state
