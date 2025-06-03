import csv
import os

class Team:
    def __init__(self, name):
        self.name = name
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def update_stats(self, goals_for, goals_against):
        self.played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
        elif goals_for == goals_against:
            self.draws += 1
            self.points += 1
        else:
            self.losses += 1

    def goal_difference(self):
        return self.goals_for - self.goals_against

    def as_list(self):
        return [self.name, self.played, self.wins, self.draws, self.losses,
                self.goals_for, self.goals_against, self.points]

def load_teams(filename="teams.csv"):
    teams = {}
    if not os.path.isfile(filename):
        print("No existing data found. Starting fresh.")
        return teams
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 8:
                continue
            t = Team(row[0])
            t.played, t.wins, t.draws, t.losses = map(int, row[1:5])
            t.goals_for, t.goals_against, t.points = map(int, row[5:8])
            teams[t.name] = t
    return teams

def save_teams(teams, filename="teams.csv"):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for team in teams.values():
            writer.writerow(team.as_list())

def enter_match_result(teams):
    team1 = input("Enter name of Team 1: ")
    team2 = input("Enter name of Team 2: ")
    if team1 not in teams or team2 not in teams:
        print("One or both teams are not registered.")
        return
    try:
        score1 = int(input(f"Score for {team1}: "))
        score2 = int(input(f"Score for {team2}: "))
    except ValueError:
        print("Invalid score. Must be a number.")
        return
    teams[team1].update_stats(score1, score2)
    teams[team2].update_stats(score2, score1)
    print("Match result recorded.")

def register_team(teams):
    name = input("Enter new team name: ")
    if name in teams:
        print("That team already exists.")
    else:
        teams[name] = Team(name)
        print(f"Team '{name}' registered successfully.")

def show_table(teams):
    sorted_teams = sorted(teams.values(), key=lambda x: (x.points, x.goal_difference()), reverse=True)
    print("\nTournament Table:")
    print(f"{'Team':15} {'P':>2} {'W':>2} {'D':>2} {'L':>2} {'GF':>3} {'GA':>3} {'GD':>3} {'Pts':>3}")
    for team in sorted_teams:
        print(f"{team.name:15} {team.played:2} {team.wins:2} {team.draws:2} {team.losses:2} "
              f"{team.goals_for:3} {team.goals_against:3} {team.goal_difference():3} {team.points:3}")

def main():
    teams = load_teams()
    while True:
        print("\n1. Register a team")
        print("2. Enter a match result")
        print("3. View tournament table")
        print("4. Save and exit")
        choice = input("Select an option: ")
        if choice == "1":
            register_team(teams)
        elif choice == "2":
            enter_match_result(teams)
        elif choice == "3":
            show_table(teams)
        elif choice == "4":
            save_teams(teams)
            print("All data saved!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
