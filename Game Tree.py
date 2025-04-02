import itertools
import random

class GameTreeNode:
    def __init__(self, sequence, player_score, opponent_score, player_turn=True):
        self.sequence = sequence
        self.player_score = player_score
        self.opponent_score = opponent_score
        self.player_turn = player_turn
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Seq: {self.sequence} | P1: {self.player_score} P2: {self.opponent_score}"


def replace_pair(a, b, player_turn, player_score, opponent_score):
    pair_sum = a + b
    if pair_sum > 7:
        return 1, player_score + 1, opponent_score
    elif pair_sum < 7:
        return 3, player_score, opponent_score - 1
    else:
        return 2, player_score + 1, opponent_score + 1


def generate_game_tree(sequence, player_score=0, opponent_score=0, player_turn=True):
    root = GameTreeNode(sequence, player_score, opponent_score, player_turn)
    if len(sequence) == 1:
        return root

    for i in range(len(sequence) - 1):
        new_number, p_score, o_score = replace_pair(
            sequence[i], sequence[i + 1], player_turn, player_score, opponent_score
        )
        new_sequence = sequence[:i] + [new_number] + sequence[i + 2:]
        child_node = generate_game_tree(new_sequence, p_score, o_score, not player_turn)
        root.add_child(child_node)

    return root


def print_tree(node, depth=0):
    print("  " * depth + str(node))
    for child in node.children:
        print_tree(child, depth + 1)


# Example usage
random_sequence = [random.randint(1, 9) for _ in range(4)]
print("Initial sequence:", random_sequence)
root_node = generate_game_tree(random_sequence)
print_tree(root_node)
