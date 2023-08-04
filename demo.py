from flask import Flask, render_template, request
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('demo.html')

@app.route('/process', methods=['POST'])
def process():
    # Retrieve form values
    loc1_strategy = request.form['loc1_strategy']
    loc1_value = request.form['loc1_value']
    action1 = request.form['action1']
    value1 = request.form['value1']
    
    loc2_strategy = request.form['loc2_strategy']
    loc2_value = request.form['loc2_value']
    action2 = request.form['action2']
    # value2 = request.form['value2']

    loc3_strategy = request.form['loc3_strategy']
    loc3_value = request.form['loc3_value']
    action3 = request.form['action3']

    loc4_strategy = request.form['loc4_strategy']
    loc4_value = request.form['loc4_value']
    action4 = request.form['action4']

    loc5_strategy = request.form.get('loc5_strategy')
    loc5_value = request.form.get('loc5_value')
    action5 = request.form.get('action5')
    
    prompt5_text = request.form.get('prompt5_text')
    prompt5_recipient = request.form.get('prompt5_recipient')
    prompt5_subject = request.form.get('prompt5_subject')
    
    prompt6_text = request.form.get('prompt6_text')
    prompt6_action = request.form.get('prompt6_action')

    loc7_strategy = request.form.get('loc7_strategy')
    loc7_value = request.form.get('loc7_value')
    action7 = request.form.get('action7')

    loc8_strategy = request.form.get('loc8_strategy')
    loc8_value = request.form.get('loc8_value')
    action8 = request.form.get('action8')

    loc9_strategy = request.form.get('loc9_strategy')
    loc9_value = request.form.get('loc9_value')
    action9 = request.form.get('action9')

    loc10_strategy = request.form.get('loc10_strategy')
    loc10_value = request.form.get('loc10_value')
    action10 = request.form.get('action10')



    # Create dictionary
    data = [
        {
            'locator_strategy': loc1_strategy,
            'locator_value': loc1_value,
            'action': action1,
            'value': value1
        },
        {
            'locator_strategy': loc2_strategy,
            'locator_value': loc2_value,
            'action': action2,
            # 'value': value2
        },
        {
            'locator_strategy': loc3_strategy,
            'locator_value': loc3_value,
            'action': action3
        },
        {
            'locator_strategy': loc4_strategy,
            'locator_value': loc4_value,
            'action': action4
        },
        {
        'locator_strategy': loc5_strategy,
        'locator_value': loc5_value,
        'action': action5,
        'prompts': [
            {
                'prompt_text': prompt5_text,
                'email_recipient': prompt5_recipient,
                'email_subject': prompt5_subject
            },
            {
                'prompt_text': prompt6_text,
                'action': prompt6_action
            }
        
                    ]
        },

        {
        'locator_strategy': loc7_strategy,
        'locator_value': loc7_value,
        'action': action7
        },
    
        {
        'locator_strategy': loc8_strategy,
        'locator_value': loc8_value,
        'action': action8
        },
    
        {
        'locator_strategy': loc9_strategy,
        'locator_value': loc9_value,
        'action': action9
        },
        {
        'locator_strategy': loc10_strategy,
        'locator_value': loc10_value,
        'action': action10
        }

        # Add dictionaries for other actions and prompts as needed
    ]

    # Write data to YAML file
    with open('data.yaml', 'w') as yaml_file:
        yaml.safe_dump(data, yaml_file,sort_keys=False)

    return 'Form submitted successfully!'


if __name__ == '__main__':
    app.run(debug=True)


