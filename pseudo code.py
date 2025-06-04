import csv
import os

# Class to represent each football team
class Team:
    def __init__(self, name):
        # Initialize team stats
        self.name = name
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def update_stats(self, goals_for, goals_against):
        # Update team stats based on match result
        self.played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        if goals_for > goals_against:
            # Team won the match
            self.wins += 1
            self.points += 3
        elif goals_for == goals_against:
            # Match was a draw
            self.draws += 1
            self.points += 1
        else:
            # Team lost the match
            self.losses += 1

    def goal_difference(self):
        # Calculate goal difference
        return self.goals_for - self.goals_against

    def as_list(self):
        # Return team stats as a list for CSV writing
        return [self.name, self.played, self.wins, self.draws, self.losses,
                self.goals_for, self.goals_against, self.points]

# Load team data from a CSV file
def load_teams(filename="teams.csv"):
    teams = {}
    if not os.path.isfile(filename):
        # File doesn't exist, return empty team list
        print("No existing data found. Starting fresh.")
        return teams
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 8:
                continue  # Skip incomplete rows
            t = Team(row[0])
            # Load stats from the CSV row
            t.played, t.wins, t.draws, t.losses = map(int, row[1:5])
            t.goals_for, t.goals_against, t.points = map(int, row[5:8])
            teams[t.name] = t
    return teams

# Save team data to a CSV file
def save_teams(teams, filename="teams.csv"):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for team in teams.values():
            # Write each team's stats as a CSV row
            writer.writerow(team.as_list())

# Enter the result of a match between two teams
def enter_match_result(teams):
    # Get team names from the user
    team1 = input("Enter name of Team 1: ")
    team2 = input("Enter name of Team 2: ")
    if team1 not in teams or team2 not in teams:
        print("One or both teams are not registered.")
        return
    try:
        # Get scores from the user
        score1 = int(input(f"Score for {team1}: "))
        score2 = int(input(f"Score for {team2}: "))
    except ValueError:
        print("Invalid score. Must be a number.")
        return
    # Update stats for both teams
    teams[team1].update_stats(score1, score2)
    teams[team2].update_stats(score2, score1)
    print("Match result recorded.")

# Register a new team
def register_team(teams):
    name = input("Enter new team name: ")
    if name in teams:
        print("That team already exists.")
    else:
        # Add new team to the dictionary
        teams[name] = Team(name)
        print(f"Team '{name}' registered successfully.")

# Display the tournament standings table
def show_table(teams):
    # Sort teams by points, then goal difference
    sorted_teams = sorted(teams.values(), key=lambda x: (x.points, x.goal_difference()), reverse=True)
    print("\nTournament Table:")
    print(f"{'Team':15} {'P':>2} {'W':>2} {'D':>2} {'L':>2} {'GF':>3} {'GA':>3} {'GD':>3} {'Pts':>3}")
    for team in sorted_teams:
        # Print each team's stats in table format
        print(f"{team.name:15} {team.played:2} {team.wins:2} {team.draws:2} {team.losses:2} "
              f"{team.goals_for:3} {team.goals_against:3} {team.goal_difference():3} {team.points:3}")

# Main program loop
def main():
    teams = load_teams()  # Load existing team data
    while True:
        # Show menu options
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
            save_teams(teams)  # Save all team data before exiting
            print("All data saved to teams.csv. Goodbye!")
            break
        else:
            print("Invalid choice.")

# Start the program
if __name__ == "__main__":
    main()
