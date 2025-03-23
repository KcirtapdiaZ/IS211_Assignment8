import random
import time

def roll_die():
    return random.randint(1, 6)

# Base Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
    
    def take_turn(self, game):
        raise NotImplementedError("This method should be overridden in subclasses.")

# HumanPlayer class
class HumanPlayer(Player):
    def take_turn(self, game):
        turn_total = 0
        print(f"Player {self.name}'s turn! Current score: {self.score}")

        while True:
            roll = roll_die()
            print(f"Player {self.name} rolled a {roll}.")

            if roll == 1:
                print("Rolled a 1! No points for this turn.")
                turn_total = 0
                break
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}, Overall score: {self.score}")

                decision = input("Roll again (r) or hold (h)? ").strip().lower()
                if decision == 'h':
                    self.score += turn_total
                    print(f"Player {self.name} holds. New total score: {self.score}\n")
                    break

# ComputerPlayer class (inherits from Player)
class ComputerPlayer(Player):
    def take_turn(self, game):
        turn_total = 0
        print(f"Player {self.name}'s turn! Current score: {self.score}")

        while True:
            roll = roll_die()
            print(f"Player {self.name} rolled a {roll}.")

            if roll == 1:
                print("Rolled a 1! No points for this turn.")
                turn_total = 0
                break
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}, Overall score: {self.score}")

                # Computer's strategy
                hold_score = min(25, 100 - self.score)
                if turn_total >= hold_score:
                    self.score += turn_total
                    print(f"Player {self.name} holds. New total score: {self.score}\n")
                    break

# Factory to create Players
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type!")

# Game class
class Game:
    def __init__(self, player1_type, player2_type):
        self.target_score = 100
        self.scores = [0, 0]
        self.players = [PlayerFactory.create_player(player1_type, "Player 1"), PlayerFactory.create_player(player2_type, "Player 2")]
        self.current_player = 0

    def play(self):
        print("Welcome to Pig!")

        while max(self.scores) < self.target_score:
            turn_total = 0
            print(f"Player {self.current_player + 1}'s turn! Current score: {self.scores[self.current_player]}")

            while True:
                self.players[self.current_player].take_turn(self)

                if self.scores[self.current_player] >= self.target_score:
                    print(f"Player {self.current_player + 1} wins with {self.scores[self.current_player]} points!\n")
                    return

            self.current_player = 1 - self.current_player

        print("Game over! Thanks for playing.")

# Timed Game Proxy
class TimedGameProxy(Game):
    def __init__(self, player1_type, player2_type, time_limit=60):
        super().__init__(player1_type, player2_type)
        self.time_limit = time_limit
        self.start_time = time.time()

    def play(self):
        print("Welcome to Timed Pig!")

        while max(self.scores) < self.target_score:
            if time.time() - self.start_time > self.time_limit:
                print("Time's up! The game is over.")
                winner = 0 if self.scores[0] > self.scores[1] else 1
                print(f"Player {winner + 1} wins with {self.scores[winner]} points!\n")
                return

            turn_total = 0
            print(f"Player {self.current_player + 1}'s turn! Current score: {self.scores[self.current_player]}")

            while True:
                self.players[self.current_player].take_turn(self)

                if self.scores[self.current_player] >= self.target_score:
                    print(f"Player {self.current_player + 1} wins with {self.scores[self.current_player]} points!\n")
                    return

            self.current_player = 1 - self.current_player

        print("Game over! Thanks for playing.")

# Main function to play game
def play_game(player1_type, player2_type, timed=False):
    if timed:
        game = TimedGameProxy(player1_type, player2_type)
    else:
        game = Game(player1_type, player2_type)

    game.play()

# Sample usage (can be run with arguments like 'human', 'computer', '--timed')
if __name__ == "__main__":
    player1_type = input("Enter type of player 1 (human/computer): ").strip().lower()
    player2_type = input("Enter type of player 2 (human/computer): ").strip().lower()
    timed = input("Play timed game? (y/n): ").strip().lower() == 'y'

    play_game(player1_type, player2_type, timed)
