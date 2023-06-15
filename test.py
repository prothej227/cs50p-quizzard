import pytest
from app import QuizzardApp
from quiz import QuestionDashboard, Results
import hashlib, random, string, os
import pandas as pd
from tabulate import tabulate

@pytest.fixture
def app():
    return QuizzardApp('Journel')

def test_quizzard_app_initialization():
    user_name = "Journel Cabrillos"
    quizzard_app = QuizzardApp(user_name)

    assert quizzard_app.user_name == user_name
    assert len(quizzard_app.menu_options) == 1
    assert quizzard_app.menu_options[0]['name'] == 'choice'
    assert quizzard_app.menu_options[0]['message'] == f'Welcome, {user_name} to CS50 - QuizzardApp'
    assert len(quizzard_app.menu_options[0]['choices']) == 3
    assert quizzard_app.menu_options[0]['choices'][0] == 'Start Quiz'
    assert quizzard_app.menu_options[0]['choices'][1] == 'View High Scores'
    assert quizzard_app.menu_options[0]['choices'][2] == 'Exit'

def test_question_dashboard(monkeypatch):

    questionList = [{
        "id": 0,
        "category": "Science",
        "question": "What is the chemical symbol for gold?",
        "choices": ["Au", "Ag", "Cu", "Fe"],
        "answer": "Au"
    }]

    mock_input = 'Au'

    def mock_prompt(questions : list):
        assert questions[0]['question'] == "What is the chemical symbol for gold?" 
        return {'choice': mock_input}

    monkeypatch.setattr('PyInquirer.prompt', mock_prompt)
    qb = QuestionDashboard("Journel Cabrillos", questionList)

    userdata = qb.show_question_and_gen_userdata()
    assert userdata['user_answers'] == [mock_input]


def test_results_output_perfect_answers(capfd):



    res = Results(user_data={
        "user_name" : "Journel Cabrillos",
        "user_answers" : ["Python", "SQL", "Pandas", "DataFrame"]
    },
    correct_answer=["Python", "SQL", "Pandas", "DataFrame"]
    )

    # Display results
    res.show()

    # Create test dataframe 
    test_df = pd.DataFrame(
            {
                'Your answers' : ["Python", "SQL", "Pandas", "DataFrame"],
                'Validation' : ["✅", "✅", "✅", "✅"]
            }
        )
    
    table = tabulate(test_df, headers='keys', tablefmt='grid')

    assert capfd.readouterr().out == f"\n{'-' * 14} Results {'-' * 14}\n{table}\n{'-' * 12} Score : {res.score}% {'-' * 12}\n"

def test_results_output_wrong_answers(capfd):

    res = Results(user_data={
        "user_name" : "Journel Cabrillos",
        "user_answers" : ["Python", "MySQL", "Pandas", "DataFrame"]
    },
    correct_answer=["Python", "SQL", "Pandas", "DataFrame"]
    )

    # Display results
    res.show()

    # Create test dataframe 
    test_df = pd.DataFrame(
            {
                'Your answers' : ["Python", "MySQL", "Pandas", "DataFrame"],
                'Validation' : ["✅", "❌", "✅", "✅"]
            }
        )
    
    table = tabulate(test_df, headers='keys', tablefmt='grid')

    assert capfd.readouterr().out == f"\n{'-' * 14} Results {'-' * 14}\n{table}\n{'-' * 12} Score : {res.score}% {'-' * 12}\n"

def test_results_score():

    test_user_data = {
        "user_name" : "Journel Cabrillos",
        "user_answers" : ["Python", "MySQL", "Pandas", "DataFrame"]
    }
    test_correct_ans = ["Python", "SQL", "Pandas", "DataFrame"]

    def _cmprelst(l1, l2):
        ''' compare list l1, l2 and returns score based on similarity'''
        if len(l1) != len(l2):
            raise ValueError("l1 & l2 should have the same length.")

        t = len(l1)
        s = sum(i1 == i2 for i1, i2 in zip(l1, l2))
        score = int(round((s / t), 2)* 100)
        return score

    res = Results(test_user_data, test_correct_ans)

    test_score = _cmprelst(test_user_data['user_answers'], test_correct_ans)

    assert test_score == res.score

def test_scores_if_dumped():
    
    _isUpdated = bool()
    gen_random_alphanum = lambda length: ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def _calc_checksum(fp : str) -> str:
        ''' gets file checksum'''
        md5h = hashlib.md5()
        with open(fp, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5h.update(chunk)
        return md5h.hexdigest()
    
    prev_cksum = _calc_checksum("./data/scores.json")

    ### Exec updation actions here
    test_results = Results({"user_name":gen_random_alphanum(5), "user_answers":['1', '1', '1', '1']}, ['1', '1', '1', '1'])
    test_results.dump_scores()                  

    new_cksum = _calc_checksum("./data/scores.json")

    assert new_cksum != prev_cksum 

def test_certs_if_exist():

    from datetime import datetime
    gen_random_alphanum = lambda length: ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    test_user_name = gen_random_alphanum(5)
    
    test_cert_path = f"certs/{test_user_name.lower().strip().replace(' ', '')}_{datetime.now().strftime('%m%d%Y')}.pdf"
    test_results = Results({"user_name": test_user_name, "user_answers":['1', '1', '1', '1']}, ['1', '1', '1', '1'])
    test_results.show_certificate_dialog()

    assert os.path.isfile(test_cert_path) == True
    


    


