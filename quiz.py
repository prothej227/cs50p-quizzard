from PyInquirer import prompt, Separator
from tabulate import tabulate
import pandas as pd
import random, json, os
from datetime import datetime
from certificate import Certificate

class Results:
    def __init__(self, user_data, correct_answer):
        self.username = user_data['user_name']
        self.ua = user_data['user_answers']
        self.ca = correct_answer

    @property
    def score(self) -> int:
        n_correct_ans = len([j for j in self.check_results() if j])
        return int(round(n_correct_ans/len(self.ca), 2) * 100)

    def check_results(self) -> list:
        ret_list = list()
        for j, ans in enumerate(self.ua):
            if ans == self.ca[j]:
                ret_list.append(True)
            else:
                ret_list.append(False)
        return ret_list

    def show(self):

        df = pd.DataFrame(
            {
                'Your answers' : self.ua,
                'Validation' : ["✅" if j else "❌" for j in self.check_results()]
            }
        )

        table = tabulate(df, headers='keys', tablefmt='grid')
        
        print("\n")
        print("-" * 14 + " Results " + "-" * 14)
        print(table)
        print("-" * 12 + f" Score : {self.score}% " + "-" * 12)
        
        

    def show_certificate_dialog(self):

        print("\n\n")
        if self.score >= 80:

            print(f"Congrats, {self.username}! You are awarded with a certificate.")

            print("Processing your certificate ...")
            cert = Certificate(username=self.username, score=self.score)
            cert_fpath = f"certs/{self.username.lower().strip().replace(' ', '')}_{datetime.now().strftime('%m%d%Y')}.pdf"
            cert.output(cert_fpath)
            print(f"****** View your certificate: {os.path.abspath(cert_fpath)} ****** ")

        else:
            print(f"Still a good job, {self.username}. You can try your luck again next time.")
        print("\n\n")

    
    def dump_scores(self):
        with open("data/scores.json") as f:
            scores = json.load(f)
        
        new_data_entry = {
            "username" : self.username,
            "score" : self.score,
            "date" : datetime.now().strftime("%m-%d-%Y")
        }

        scores.append(new_data_entry)

        with open("data/scores.json", "w") as f:
            json.dump(scores, f)


class QuestionDashboard:

    def __init__(self, username : str, questions : list) -> None:
        self._username = username
        self.questions = questions
        self.current_question = 0
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        self._username = value

    def show_question_and_gen_userdata(self) -> list:

        _userdata = {
            "user_name" : self.username,
            "user_answers" : []
        }

        for i, question in enumerate(self.questions):
            str_head = "-" * int(len(question['question'])/2) + f" Question No. {i+1} " + "-" * int(len(question['question'])/2) 
            print(str_head)
            self.menu_options = [
                {
                    'type': 'list',
                    'name': 'choice',
                    'message': question['question'],
                    'choices': question['choices']
                },
            ]
            answers = prompt(self.menu_options)
            _userdata['user_answers'].append(answers['choice'])
            print("-" * len(str_head) + "\n")
        return _userdata

# Test program here   
if __name__ == "__main__":

    with open('./data/questions.json') as f:
        q1 = json.loads(f.read())

    for question in q1:
        random.shuffle(question['choices'])

    qb = QuestionDashboard(username=input("Type name: "), questions=q1)
    user1_data = qb.show_question_and_gen_userdata()
    res = Results(user_data=user1_data, correct_answer=[j['answer'] for j in q1])
    res.display_results()