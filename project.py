from PyInquirer import prompt
from tabulate import tabulate
from quiz import QuestionDashboard, Results
import json, random
import pandas as pd
import sys

class QuizzardApp:

    ''' Quizzard Main UI'''

    def __init__(self, user_name) -> None:
        self.user_name = user_name
        self.menu_options = [
            
            {
                'type': 'list',
                'name': 'choice',
                'message': f'Welcome, {self.user_name} to CS50 - QuizzardApp',
                'choices': [
                    'Start Quiz',
                    'View High Scores',
                    'Exit'
                ]
            }
        ]

    def run(self):

        self.show_menu()

    def show_menu(self):
        
        answers = prompt(self.menu_options)
        choice = answers['choice']

        if choice == 'Start Quiz':
            self.start_quiz()
        elif choice == 'View High Scores':
            self.view_high_scores()
        elif choice == 'Exit':
            print("Exiting QuizzardApp...")
            sys.exit(0)

    def start_quiz(self):

        print(f"\nGood luck, {self.user_name}!\n")
        with open('./data/questions.json') as f:
            q1 = json.loads(f.read())

        q1 = random.sample(list(q1), 10)

        for question in q1:
            random.shuffle(question['choices'])

        NewQuestionBoard = QuestionDashboard(self.user_name, q1)
        user_data = NewQuestionBoard.show_question_and_gen_userdata()

        self.result = Results(user_data, [j['answer'] for j in q1])
        self.show_post_quiz_results()

    def show_post_quiz_results(self):

        print("\n")

        response = prompt([
        {
            'type': 'list',
            'name': 'choice',
            'message': "Do you want to view your results and claim your certificate?",
            'choices': ["Yes", "No, Back to Menu"]
        }
        ])

        self.result.dump_scores()

        if response['choice'] == 'Yes':

            # !Important methods to that nees to be executed
            self.result.show()
            self.result.show_certificate_dialog()


            menu_with_no_start = self.menu_options
            menu_with_no_start[0]['choices'].pop(0) 
            print("--------------------------------")
            ch = prompt(menu_with_no_start)['choice']
            if ch == 'View High Scores':
                self.view_high_scores()
            elif ch == "Exit":
                print("Exiting...")
        else:

            menu_with_no_start = self.menu_options
            menu_with_no_start[0]['choices'].pop(0) 

            print("\n")
            ch = prompt(menu_with_no_start)['choice']

            if ch == 'View High Scores':
                self.view_high_scores()
            elif ch == "Exit":
                print("Exiting...")


    def view_high_scores(self):

        with open('data/scores.json', 'r') as file:
            scores = json.load(file)
        df = pd.DataFrame(scores)

        print(""" 

 __ __  ___       _____  _____  _____  _____  _____  _____ 
/  |  \/___\ ___ /  ___>/     \/  _  \/  _  \/   __\/  ___>
|  _  ||   |<___>|___  ||  |--||  |  ||  _  <|   __||___  |
\__|__/\___/     <_____/\_____/\_____/\__|\_/\_____/<_____/
                                                                                                      
        """)

        try:

            df = df.sort_values(by="score", ascending=False)
            df = df.reset_index(drop=True)
            df = df.rename_axis('Rank')
            df.columns = df.columns.str.title()
            df.index = df.index + 1
            table = tabulate(df, headers='keys', tablefmt='grid')
            print(table)

        except:
            print("No scores data.")


# Entry point of the program
if __name__ == "__main__":

    print("""\n
     __/\__
. _  \/\/''//
-( )-/_||_\/
 .'. \_()_/
  |   | . \/
  |mrf| .  \/
 .'. ,\_____'.
    _______  __   __  ___   _______  _______  _______  ______    ______  
    |       ||  | |  ||   | |       ||       ||   _   ||    _ |  |      | 
    |   _   ||  | |  ||   | |____   ||____   ||  |_|  ||   | ||  |  _    |
    |  | |  ||  |_|  ||   |  ____|  | ____|  ||       ||   |_||_ | | |   |
    |  |_|  ||       ||   | | ______|| ______||       ||    __  || |_|   |
    |      | |       ||   | | |_____ | |_____ |   _   ||   |  | ||       |
    |____||_||_______||___| |_______||_______||__| |__||___|  |_||______|    
\n    
----------------------------------------------
    A python-based quiz game.
    Author: journelcabrillos@gmail.com   
----------------------------------------------

    \n""")
    app = QuizzardApp(input("Type name: "))
    app.run()