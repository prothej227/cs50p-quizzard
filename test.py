from PyInquirer import prompt

def prompt_color(answers):
    name = answers['name']
    questions = [
        {
            'type': 'list',
            'name': 'color',
            'message': f"Select a color, {name}:",
            'choices': ['Red', 'Blue', 'Green'],
        }
    ]
    return prompt(questions)['color']

questions = [
    {
        'type': 'input',
        'name': 'name',
        'message': 'Enter your name',
    },
    {
        'type': 'list',
        'name': 'color',
        'message': lambda answers: f"Select a color, {answers['name']}:",
        'choices': prompt_color,
    },
]

answers = prompt(questions)
name_value = answers['name']
color_value = answers['color']
print('Name:', name_value)
print('Color:', color_value)