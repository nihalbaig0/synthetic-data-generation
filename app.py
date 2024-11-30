import json
import random
from flask import Flask, render_template, request, send_file
from io import BytesIO

app = Flask(__name__)

# Load field definitions from JSON file
with open('field_definitions.json', 'r', encoding='utf-8') as f:
    FIELD_DEFINITIONS = json.load(f)

def generate_synthetic_data():
    data = {}
    for section, section_data in FIELD_DEFINITIONS.items():
        data[section] = {}
        for field, properties in section_data['fields'].items():
            if properties['type'] == 'text':
                data[section][field] = ''.join(random.choices('অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ', k=random.randint(5, 10)))
            elif properties['type'] == 'number':
                data[section][field] = random.randint(properties['min'], properties['max'])
            elif properties['type'] == 'date':
                data[section][field] = f"{random.randint(1950, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            elif properties['type'] == 'select':
                data[section][field] = random.choice(properties['options'])
    return data

def generate_input_html(field, properties, value):
    if properties['input_style'] == 'single-line':
        return f'<input type="text" id="{field}" name="{field}" value="{value}" maxlength="{properties["char_count"]}">'
    elif properties['input_style'] == 'multi-line':
        return f'<textarea id="{field}" name="{field}" rows="{properties["rows"]}" cols="{properties["cols"]}">{value}</textarea>'
    elif properties['input_style'] == 'boxed-chars':
        html = '<div class="boxed-chars-container">'
        for char in value:
            html += f'<input type="text" class="boxed-chars-input" value="{char}" maxlength="1">'
        html += '</div>'
        return html
    elif properties['input_style'] == 'dotted-line':
        return f'<input type="text" id="{field}" name="{field}" value="{value}" class="dotted-line">'
    elif properties['input_style'] == 'dropdown':
        html = f'<select id="{field}" name="{field}">'
        for option in properties['options']:
            selected = 'selected' if option == value else ''
            html += f'<option value="{option}" {selected}>{option}</option>'
        html += '</select>'
        return html
    elif properties['input_style'] == 'radio':
        html = '<div class="radio-group">'
        for option in properties['options']:
            checked = 'checked' if option == value else ''
            html += f'<label><input type="radio" name="{field}" value="{option}" {checked}> {option}</label>'
        html += '</div>'
        return html
    return f'<input type="text" id="{field}" name="{field}" value="{value}">'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_records = int(request.form.get('num_records', 1))
        generated_data = [generate_synthetic_data() for _ in range(num_records)]
        return render_template('form.html', data=generated_data, fields=FIELD_DEFINITIONS, generate_input_html=generate_input_html)
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    num_records = int(request.form.get('num_records', 1))
    generated_data = [generate_synthetic_data() for _ in range(num_records)]
    json_data = json.dumps(generated_data, ensure_ascii=False, indent=2)
    buffer = BytesIO()
    buffer.write(json_data.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, mimetype='application/json', as_attachment=True, download_name='synthetic_data.json')

if __name__ == '__main__':
    app.run(debug=True)