from flask import Flask, request, render_template, redirect, url_for, flash
import json
from todo_app.flask_config import Config
from todo_app.data import session_items as session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=["GET"])
def index():
    sort_status = request.args.get('sort_by_status', 'DESC')
    items = sorted(session.get_items(), key=lambda x: x['status'], reverse=False if sort_status == 'ASC' else True)
    return render_template('index.html', todos=items)

@app.route('/', methods=["POST"])
def save_item():
    title = request.form.get('title', '').strip()
    if title == '':
        flash('Please enter a task')
    else:
        session.add_item(title)        

    return redirect(url_for('index'))

@app.route('/mark-completed', methods=["POST"])
def mark_completed():
    todo_id = request.form['todo_id']
    item = session.get_item(todo_id)
    item['status'] = 'Completed'
    session.save_item(item)
    return redirect(url_for('index'))

@app.route('/delete-item', methods=["POST"])
def delete_item():
    todo_id = request.form['todo_id']
    item = session.get_item(todo_id)
    session.remove_item(item)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
