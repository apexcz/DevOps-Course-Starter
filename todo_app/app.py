from flask import Flask, request, render_template, redirect, url_for
import json
from todo_app.flask_config import Config
from todo_app.data import session_items as session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=["GET", "POST"])
def index():
    error_message = None
    if request.method == "POST":
        title = request.form.get('title', '').strip()
        if title == '':
            error_message = 'Please enter a task'
        else:
            session.add_item(title)        

    sort_status = request.args.get('sort_by_status', 'DESC')
    items = sorted(session.get_items(), key=lambda x: x['status'], reverse=False if sort_status == 'ASC' else True)
    return render_template('index.html', todos=items, error=error_message)

@app.route('/mark-completed', methods=["POST"])
def mark_completed():
    item = json.loads(request.form['todo_item'])
    item['status'] = 'Completed'
    session.save_item(item)
    return redirect(url_for('index'))

@app.route('/delete-item', methods=["POST"])
def delete_item():
    item = json.loads(request.form['todo_item'])
    session.remove_item(item)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
