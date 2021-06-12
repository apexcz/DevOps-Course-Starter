from datetime import date
from flask import Flask, request, render_template, redirect, url_for, flash
from todo_app.flask_config import Config
from todo_app.service import ItemService
from todo_app.view_model import ViewModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    service = ItemService()

    @app.route('/', methods=["GET"])
    def index():
        item_view_model = ViewModel(service.get_all_items())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/', methods=["POST"])
    def save_item():
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due-date', '').strip()

        if validate_input(title, due_date):
            service.create_item(title, description, due_date)

        return redirect(url_for('index'))

    @app.route('/move-to-doing', methods=["POST"])
    def move_to_doing():
        todo_id = request.form['todo_id']
        service.move_to_doing(todo_id)
        return redirect(url_for('index'))

    @app.route('/move-to-done', methods=["POST"])
    def move_to_done():
        todo_id = request.form['todo_id']
        service.move_to_done(todo_id)
        return redirect(url_for('index'))

    @app.route('/move-to-todo', methods=["POST"])
    def move_to_todo():
        todo_id = request.form['todo_id']
        service.move_to_todo(todo_id)
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

    return app
