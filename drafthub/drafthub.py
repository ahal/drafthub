import os

from flask import (
    Flask,
    render_template,
    request,
)

here = os.path.abspath(os.path.dirname(__file__))


app = Flask('drafthub')

@app.route('/', methods=['GET', 'POST'])
def drafthub():
    if request.method == 'POST':
        csv_file = request.files['csv_path']
        lines = csv_file.readlines()

        header = tokenize(lines.pop(0))
        for i, td in enumerate(header):
            if isinstance(td, basestring) and td.lower() in ('name', 'player'):
                print(i)
                player_index = i
                break
        else:
            player_index = None

        context = {
            'header': header,
            'players': [],
            'player_index': player_index,
        }
        for line in lines:
            line = line.decode('utf8', 'replace')
            context['players'].append(tokenize(line))
        return render_template('draft.html', **context)
    return render_template('upload.html')

def tokenize(line):
    return [t.strip('"') for t in line.split(',')]

if __name__ == '__main__':
    app.run(debug=True)
