import csv
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
        reader = csv.reader(request.files['csv_path'])
        lines = []
        for row in reader:
            lines.append(row)

        header = lines.pop(0)
        for i, td in enumerate(header):
            if isinstance(td, basestring) and td.lower() in ('name', 'player'):
                player_index = i
                break
        else:
            player_index = None

        context = {
            'header': header,
            'players': lines,
            'player_index': player_index,
        }
        return render_template('draft.html', **context)
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
