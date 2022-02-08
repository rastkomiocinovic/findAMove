import random
import numpy as np

from agents import Agent


# Example agent, behaves randomly.
# ONLY StudentAgent and his descendants have a 0 id. ONLY one agent of this type must be present in a game.
# Agents from bots.py have successive ids in a range from 1 to number_of_bots.
class StudentAgent(Agent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)
        self.id = 0

    @staticmethod
    def kind():
        return '0'

    # Student shall override this method in derived classes.
    # This method should return one of the legal actions (from the Actions class) for the current state.
    # state - represents a state object.
    # max_levels - maximum depth in a tree search. If max_levels eq -1 than the tree search depth is unlimited.
    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)  # equivalent of state.get_legal_actions(self.id)
        chosen_action = actions[random.randint(0, len(actions) - 1)]
        # Example of a new_state creation (for a chosen_action of a self.id agent):
        # new_state = state.apply_action(self.id, chosen_action)
        return chosen_action


def is_end(state, max_id, min_id):
    if len(state.get_legal_actions(max_id)) == 0:
        return -1
    if len(state.get_legal_actions(min_id)) == 0:
        return 1
    return 0


class MinimaxAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        max_id = self.get_id()
        min_id = (max_id + 1) % 2
        (s, m) = self.max(state, max_levels, max_id, min_id)
        print(max_id, s)
        if s == 1:
            return m
        return state.get_legal_actions(max_id)[0]

    def max(self, state, max_levels, max_id, min_id):
        score = -2
        move = ''

        if max_levels == 0:
            return 0, ''

        if is_end(state, max_id, min_id) == 1:
            return 1, ''
        if is_end(state, max_id, min_id) == -1:
            return -1, ''

        actions = state.get_legal_actions(max_id)
        for a in actions:
            next_state = state.apply_action(max_id, a)
            (s, m) = self.min(next_state, max_levels - 1, max_id, min_id)
            if s > score:
                score = s
                move = a
        return score, move

    def min(self, state, max_levels, max_id, min_id):
        score = 2
        move = ''

        if max_levels == 0:
            return 0, ''

        if is_end(state, max_id, min_id) == 1:
            return 1, ''
        if is_end(state, max_id, min_id) == -1:
            return -1, ''

        actions = state.get_legal_actions(min_id)
        for a in actions:
            next_state = state.apply_action(min_id, a)
            (s, m) = self.max(next_state, max_levels - 1, max_id, min_id)
            if s < score:
                score = s
                move = a
        return score, move



class MinimaxABAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        max_id = self.get_id()
        min_id = (max_id + 1) % 2
        (s, m) = self.max(state, max_levels, max_id, min_id, -2, 2)
        print(max_id, s)
        if s == 1:
            return m
        return state.get_legal_actions(max_id)[0]

    def max(self, state, max_levels, max_id, min_id, alpha, beta):
        score = -2
        move = ''

        if max_levels == 0:
            return 0, ''

        if is_end(state, max_id, min_id) == 1:
            return 1, ''
        if is_end(state, max_id, min_id) == -1:
            return -1, ''

        actions = state.get_legal_actions(max_id)
        for a in actions:
            next_state = state.apply_action(max_id, a)
            (s, m) = self.min(next_state, max_levels - 1, max_id, min_id, alpha, beta)
            if s > score:
                score = s
                move = a

            if s > alpha:
                alpha = s
            if alpha > beta:
                return score, a
        return score, move

    def min(self, state, max_levels, max_id, min_id, alpha, beta):
        score = 2
        move = ''

        if max_levels == 0:
            return 0, ''

        if is_end(state, max_id, min_id) == 1:
            return 1, ''
        if is_end(state, max_id, min_id) == -1:
            return -1, ''

        actions = state.get_legal_actions(min_id)
        for a in actions:
            next_state = state.apply_action(min_id, a)
            (s, m) = self.max(next_state, max_levels - 1, max_id, min_id, alpha, beta)
            if s < score:
                score = s
                move = a

            if s < beta:
                beta = s
            if alpha > beta:
                return score, a
        return score, move


class ExpectAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        max_id = self.get_id()
        chance_id = (max_id + 1) % 2
        (s, m) = self.max(state, max_levels, max_id, chance_id)
        print(max_id, s)
        if s == 1:
            return m
        return state.get_legal_actions(max_id)[0]

    def max(self, state, max_levels, max_id, chance_id):
        score = -2
        move = ''

        if max_levels == 0:
            return 0, ''

        if is_end(state, max_id, chance_id) == 1:
            return 1, ''
        if is_end(state, max_id, chance_id) == -1:
            return -1, ''

        actions = state.get_legal_actions(max_id)
        for a in actions:
            next_state = state.apply_action(max_id, a)
            (s, m) = self.chance(next_state, max_levels - 1, max_id, chance_id)
            if s > score:
                score = s
                move = a
        return score, move

    def chance(self, state, max_levels, max_id, min_id):
        score = 0
        move = ''

        if max_levels == 0:
            return 0, ''

        if is_end(state, max_id, min_id) == 1:
            return 1, ''
        if is_end(state, max_id, min_id) == -1:
            return -1, ''

        actions = state.get_legal_actions(min_id)
        cnt = 0
        for a in actions:
            next_state = state.apply_action(min_id, a)
            (s, m) = self.max(next_state, max_levels - 1, max_id, min_id)
            score = score + s
            cnt = cnt + 1
        score = score / cnt
        print(score, cnt)

        return score, move


class MaxNAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        n = 3

        max_id = self.get_id()
        min_ids = []
        curr_id = max_id
        for i in range(n):
            curr_id = (curr_id + 1) % n
            min_ids.append(curr_id)
        (s, m) = self.max(state, max_levels, max_id, min_ids)
        print(max_id, s)
        if s == 1:
            return m
        return state.get_legal_actions(max_id)[0]

    def max(self, state, max_levels, max_id, min_ids):
        score = -2
        move = ''

        if max_levels == 0:
            return 0, ''

        if len(state.get_legal_actions(max_id)) == 0:
            return -1, ''
        cnt = 0
        for i in min_ids:
            if len(state.get_legal_actions(i)) == 0:
                cnt = cnt + 1
        if cnt == len(min_ids):
            return 1, ''

        actions = state.get_legal_actions(max_id)
        for a in actions:
            next_state = state.apply_action(max_id, a)
            (s, m) = self.min(next_state, max_levels - 1, max_id, min_ids)
            if s > score:
                score = s
                move = a
        return score, move

    def min(self, state, max_levels, max_id, min_ids):
        score = 2
        move = ''

        if max_levels == 0:
            return 0, ''

        if len(state.get_legal_actions(max_id)) == 0:
            return -1, ''
        cnt = 0
        for i in min_ids:
            if len(state.get_legal_actions(i)) == 0:
                cnt = cnt + 1
        if cnt == len(min_ids):
            return 1, ''

        for i in min_ids:
            actions = state.get_legal_actions(i)
            for a in actions:
                next_state = state.apply_action(i, a)
                (s, m) = self.max(next_state, max_levels - 1, max_id, min_ids)
                if s < score:
                    score = s
                    move = a
        return score, move
