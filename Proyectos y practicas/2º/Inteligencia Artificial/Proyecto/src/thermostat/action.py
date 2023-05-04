class Action():
    def __init__(self, id: str, cost: str, probabilities: dict, current_state: str):
        """
        Action is a class that contains the information of an action, such as the cost, the probabilities of
        transition to other states and the current state.
        :param id: name or descriptor of the action
        :param cost: cost of the action
        :param probabilities: dictionary containing as keys the id's of the posible transition states and as values the probabilities
        of transitioning to that state
        :param current_state: the associated state of the action
        """
        self.__id = id
        self.__current_state = current_state
        self.__cost = cost
        check = 0
        for i in probabilities:
            check += probabilities[i]
        if round(check, 10) != 1:
            raise ValueError("Transition probabilities of an action must sum 1")
        self.__probabilities = probabilities

    def __str__(self):
        asociated_state = "Asociated state: " + self.__current_state + ". "
        coste = "With cost: " + str(self.__cost) + ". "
        return self.__id + " " + asociated_state + coste

    @property
    def id(self):
        return self.__id

    @property
    def cost(self):
        return self.__cost

    @property
    def probabilities(self):
        return self.__probabilities

    @property
    def current_state(self):
        return self.__current_state
