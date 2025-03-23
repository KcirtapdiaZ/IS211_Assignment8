import random
import time

# Roll a die
def roll_die():
    return random.randint(1, 6)

# Abstract base class for Player
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def roll_or_hold(self, turn_total):
        raise NotImplementedError

# Human Player class
class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def roll_or_hold(self, turn_total):
        decision = input(f"{self.name}, Roll again (r) or hold (h)? ").strip().lower()
        return decision == 'h'

# Computer Player class
class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def roll_or_hold(self, turn_total):
        # Computer strategy: hold at the lesser of 25 and 100 - score
        target_hold = min(25, 100 - self.score)
        if turn_total >= target_hold:
            print(f"{self.name} holds with a turn total of {turn_total}.")
            return True
        else:
            print(f"{self.name} rolls again with a turn total of {turn_total}.")
            return False

# Player Factory
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

# Game class
class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0
        self.target_score = 100

    def play_turn(self):
        player = self.players[self.current_player]
        print(f"\n{player.name}'s turn! Current score: {player.score}")
        turn_total = 0

        while True:
            roll = roll_die()
            print(f"{player.name} rolled a {roll}.")
            if roll == 1:
                print(f"Rolled a 1! No points for this turn.")
                turn_total = 0
                break
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}, Overall score: {player.score}")

                if player.roll_or_hold(turn_total):
                    player.score += turn_total
                    print(f"{player.name} holds. New total score: {player.score}\n")
                    break

        if player.score >= self.target_score:
            print(f"{player.name} wins with {player.score} points!\n")
            return True  # Game ends if a player reaches target score
        return False

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def play(self):
        while True:
            if self.play_turn():
                break
            self.switch_player()

# Timed Game Proxy
class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play_turn(self):
        # Check if one minute has passed
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 60:
            print("Time's up! The game will end now.")
            return True  # Time is up, end the game
        return self.game.play_turn()

    def play(self):
        while True:
            if self.play_turn():
                break
            self.game.switch_player()

# Main function to start the game
def play_game(player1_type, player2_type, timed=False):
    player1 = PlayerFactory.create_player(player1_type, "Player 1")
    player2 = PlayerFactory.create_player(player2_type, "Player 2")

    game = Game(player1, player2)

    if timed:
        game = TimedGameProxy(game)

    print("Welcome to the Timed Pig Game!" if timed else "Welcome to Pig!")
    game.play()

# Entry point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Play the game of Pig.")
    parser.add_argument('--player1', choices=['human', 'computer'], default='human', help="Player 1 type (human/computer)")
    parser.add_argument('--player2', choices=['human', 'computer'], default='human', help="Player 2 type (human/computer)")
    parser.add_argument('--timed', action='store_true', help="Enable timed game")

    args = parser.parse_args()
    play_game(args.player1, args.player2, args.timed)
