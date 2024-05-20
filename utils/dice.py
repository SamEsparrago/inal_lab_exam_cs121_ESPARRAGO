import random
import os
import time
from utils.score import Score

class DiceGame:
    def __init__(self, username):
        self.username = username
        self.score_folder = "scores"
        self.score_file = os.path.join(self.score_folder, "top_scores.txt")
        self.create_score_folder()
        self.score = Score(self.username, "")

    def create_score_folder(self):
        if not os.path.exists(self.score_folder):
            os.makedirs(self.score_folder)
        
    def load_scores(self):
        scores = []
        try:
            if os.path.exists(self.score_file):
                with open(self.score_file, "r") as file:
                    for line in file:
                        username, points, stage_score, game_id = line.strip().split(",")
                        scores.append((username, int(points), int(stage_score), game_id))
            return scores
        except FileNotFoundError:
            return []

    def save_scores(self, scores):
        with open(self.score_file, "w") as file:
            for username, points, stage_score, game_id in scores:
                file.write(f"{username},{points},{stage_score},{game_id}\n")

    def top_scores(self):
        top_scores = self.load_scores()
        top_scores.append(self.score.set_game_id_date())
        top_scores.sort(key=lambda i: i[1], reverse=True) 
        top_scores = top_scores[:10] 
        self.save_scores(top_scores) 

    def show_top_scores(self):
        os.system('cls')
        scores = self.load_scores()
        
        if not scores:
            print("No played yet. Play game see most scores.")
        else:
            print("Top scores:")
            for idx, (username, score, stage, game_id) in enumerate(scores, start=1):
                print(f"{idx}. {username}: Points - {score}, Wins - {stage}, {game_id}")
        input("\nPress Enter to Continue...")
        
    def play_game(self):
        os.system('cls')
        print(f"Starting game as {self.username}...\n")

        points = {"user": 0, "cpu": 0, "points": 0, "stage": 0} 
        tie = 0
        stage = 1

        while True:
            while True:
                if tie > 1:
                    if points["user"] == 1 or points["cpu"] == 1:
                        break
                else:
                    if points["user"] == 2 or points["cpu"] == 2:
                        break
                    else:
                        cpu_roll = random.randint(1, 6)
                        user_roll = random.randint(1, 6)
                        time.sleep(0.5)
                        print(f"{self.username} rolled: {user_roll}")
                        time.sleep(0.5)
                        print(f"Computer rolled: {cpu_roll}")
                        time.sleep(0.5)
                        if user_roll > cpu_roll:
                            print(f"{self.username} wins this round!\n")
                            points["user"] += 1
                            points["points"] += 1
                        elif user_roll < cpu_roll:
                            print("CPU wins this round!\n")
                            points["cpu"] += 1
                        else:
                            print("It's a tie!\n")
                            tie += 1
                        time.sleep(1)

            if points["user"] != points["cpu"]:
                if points["user"] > points["cpu"]:
                    winner = "user"
                else:
                    winner = "cpu"
                    
                if winner == "user":
                    print(f"You won this stage, {self.username}")
                    points["points"] += 3
                    points["stage"] += 1
                    stage += 1

                 
                    self.score.update_score(points["points"], points["stage"])
                    print("Total Points:", points["points"], ", Stages Won:", points["stage"])
                    time.sleep(1)

                    while True:
                        try:
                            option = input("\nDo you want to continue to the next stage? (1 for 'Yes' 0 for 'No'): ")
                            if option == "1":
                                points["user"] = 0
                                points["cpu"] = 0
                                os.system("cls")
                                print(f"Starting game as {self.username}...\n")
                                break
                            elif option == "0":
                                self.score.update_score(points["points"], points["stage"])
                                self.top_scores()
                                print(f"Game over. You won", points["stage"], "stage(s) with a total of", points["points"], "points.")
                                self.score.points = 0
                                self.score.stage_score = 0
                                time.sleep(1)
                                input("\nPress ENTER to continue.")
                                self.menu()
                                return
                            else:
                                print("Invalid input. Please enter 1 for 'Yes' or 0 for 'No'.")
                                time.sleep(1)
                        except ValueError as e:
                            print(f"Error: {e}. Invalid input.")
                else:
                    print(f"You lost this stage, {self.username}.")
                    print("Game over. ", end="")
                    self.score.update_score(points["points"], points["stage"])
                    if points["stage"] == 0:
                        print("You didn't win any stages.")
                    else:
                        print(f"Total Points: {points['points']}, Stages Won: {points['stage']}")
                        self.top_scores()
                    input("\nPress Enter to Continue...")
                    return
            else:
                print("nice one")

    def logout(self):
        os.system('cls')
        print("Logging out...")
        time.sleep(1)
        os.system('cls')
        return True

    def menu(self):
        while True:
            os.system('cls')
            print(f"Welcome, {self.username}!")
            print("Menu:")
            print("1. Start game")
            print("2. Show top scores")
            print("3. Log out")
            choice = input("Enter your choice, or leave blank to cancel: ")
            if not choice:
                break
            if choice == "1":
                self.play_game()
            elif choice == "2":
                self.show_top_scores()
            elif choice == "3":
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)