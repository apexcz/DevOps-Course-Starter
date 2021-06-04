from datetime import date
from flask import Flask, request, render_template, redirect, url_for, flash
from todo_app.flask_config import Config
from todo_app.service import ItemService

app = Flask(__name__)
app.config.from_object(Config)

service = ItemService(app)

@app.route('/', methods=["GET"])
def index():
    sort_status = request.args.get('sort_by_status', 'DESC')
    items = sorted(service.get_all_items(), key=lambda x: x.status,
                   reverse=False if sort_status == 'ASC' else True)
    return render_template('index.html', todos=items)


@app.route('/', methods=["POST"])
def save_item():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due-date', '').strip()

    if validate_input(title, due_date):
        service.create_item(title, description, due_date)

    return redirect(url_for('index'))


@app.route('/complete-item', methods=["POST"])
def complete_item():
    todo_id = request.form['todo_id']
    service.complete_item(todo_id)
    return redirect(url_for('index'))


@app.route('/repeat-item', methods=["POST"])
def repeat_item():
    todo_id = request.form['todo_id']
    service.repeat_item(todo_id)
    return redirect(url_for('index'))


@app.route('/delete-item', methods=["POST"])
def delete_item():
    todo_id = request.form['todo_id']
    service.delete_item(todo_id)
    return redirect(url_for('index'))


def validate_input(title_input, date_input):
    if title_input == '':
        flash('Please enter a task')
        return False
    if date_input:
        chosen_date = date.fromisoformat(date_input)
        if date.today() > chosen_date:
            flash('Please enter a valid date in the future')
            return False
    return True


if __name__ == '__main__':
    app.run()
