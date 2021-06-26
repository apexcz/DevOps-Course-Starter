from datetime import date
from dotenv import load_dotenv, find_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from threading import Thread
from todo_app import app
from todo_app.board import Board


@pytest.fixture(scope='module')
def driver():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')

    with webdriver.Chrome(options=opts) as driver:
        yield driver


@pytest.fixture(scope='module')
def app_with_temp_board():
    os.environ['TRELLO_BOARD_NAME'] = 'DummyBoard'
    board_id = Board.create_board(os.environ.get('TRELLO_API_KEY'), os.environ.get(
        'TRELLO_TOKEN'), os.environ.get('TRELLO_BOARD_NAME'))

    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    Board.delete_board(os.environ.get('TRELLO_API_KEY'),
                       os.environ.get('TRELLO_TOKEN'), board_id)


@pytest.fixture(scope='function', autouse=True)
def clean_board():
    yield
    board = Board()
    todo_list_id = board.get_todo_list_id()
    doing_list_id = board.get_doing_list_id()
    done_list_id = board.get_done_list_id()

    Board.archive_cards(os.environ.get('TRELLO_API_KEY'),
                        os.environ.get('TRELLO_TOKEN'), todo_list_id)
    Board.archive_cards(os.environ.get('TRELLO_API_KEY'),
                        os.environ.get('TRELLO_TOKEN'), doing_list_id)
    Board.archive_cards(os.environ.get('TRELLO_API_KEY'),
                        os.environ.get('TRELLO_TOKEN'), done_list_id)


def test_tasks_are_empty_on_startup(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert 'To-Do App' in driver.title


def test_add_tasks_and_displays_alphabetically(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    wait = WebDriverWait(driver, 10)

    title_field = driver.find_element_by_id("title")
    title_field.send_keys('Do grocery shopping')
    title_field.submit()

    new_todo_row = wait.until(
        EC.visibility_of_element_located((By.ID, 'not-started-1')))

    assert 'Do grocery shopping' in new_todo_row.text

    title_field = driver.find_element_by_id("title")
    description_field = driver.find_element_by_id("description")
    due_date_field = driver.find_element_by_id("due-date")

    future_year = date.today().year + 1
    future_date = f'19/03/{future_year}'

    title_field.clear()
    title_field.send_keys('Take a nap')
    description_field.send_keys('Sleep for at least 30 minutes')
    due_date_field.send_keys(future_date)
    due_date_field.submit()
    wait.until(EC.visibility_of_element_located((By.ID, 'not-started-2')))

    title_field = driver.find_element_by_id("title")
    title_field.clear()
    title_field.send_keys('Have lunch')
    title_field.submit()
    wait.until(EC.visibility_of_element_located((By.ID, 'not-started-3')))

    first_row = driver.find_element_by_id("not-started-1")
    second_row = driver.find_element_by_id("not-started-2")
    third_row = driver.find_element_by_id("not-started-3")

    assert 'Do grocery shopping' in first_row.text
    assert 'Have lunch' in second_row.text
    assert 'Take a nap' in third_row.text


def test_add_tasks_past_due_date_fails(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    wait = WebDriverWait(driver, 10)

    title_field = driver.find_element_by_id("title")
    due_date_field = driver.find_element_by_id("due-date")

    title_field.send_keys('Go to the park')
    due_date_field.send_keys('10/01/2021')
    due_date_field.submit()
    error_message = wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, 'error-message')))

    assert 'Please enter a valid date in the future' in error_message.text


def test_move_item_to_in_progress(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    wait = WebDriverWait(driver, 10)

    title_field = driver.find_element_by_id("title")
    title_field.send_keys('Do grocery shopping')
    title_field.submit()

    wait.until(EC.visibility_of_element_located((By.ID, 'not-started-1')))

    todo_table = driver.find_element_by_id("not-started")
    in_progress_table = driver.find_element_by_id("in-progress")

    assert 'Do grocery shopping' in todo_table.text
    assert 'Do grocery shopping' not in in_progress_table.text

    start_btn = driver.find_element_by_id("start-1")
    start_btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, 'in-progress-1')))
    todo_table = driver.find_element_by_id("not-started")
    in_progress_table = driver.find_element_by_id("in-progress")

    assert 'Do grocery shopping' not in todo_table.text
    assert 'Do grocery shopping' in in_progress_table.text


def test_move_item_to_completed(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    wait = WebDriverWait(driver, 10)

    title_field = driver.find_element_by_id("title")
    title_field.send_keys('Do grocery shopping')
    title_field.submit()
    wait.until(EC.visibility_of_element_located((By.ID, 'not-started-1')))

    start_btn = driver.find_element_by_id("start-1")
    start_btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, 'in-progress-1')))

    completed_table = driver.find_element_by_id("completed")

    assert 'Do grocery shopping' not in completed_table.text

    done_btn = driver.find_element_by_id("done-1")
    done_btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, 'completed-1')))
    completed_table = driver.find_element_by_id("completed")

    assert 'Do grocery shopping' in completed_table.text


def test_repeat_item(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    wait = WebDriverWait(driver, 10)

    title_field = driver.find_element_by_id("title")
    title_field.send_keys('Do grocery shopping')
    title_field.submit()
    wait.until(EC.visibility_of_element_located((By.ID, 'not-started-1')))

    start_btn = driver.find_element_by_id("start-1")
    start_btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, 'in-progress-1')))

    done_btn = driver.find_element_by_id("done-1")
    done_btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, 'completed-1')))

    todo_table = driver.find_element_by_id("not-started")

    assert 'Do grocery shopping' not in todo_table.text

    repeat_btn = driver.find_element_by_id("repeat-1")
    repeat_btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, 'not-started-1')))

    todo_table = driver.find_element_by_id("not-started")
    assert 'Do grocery shopping' in todo_table.text


def test_delete_item(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    wait = WebDriverWait(driver, 10)

    title_field = driver.find_element_by_id("title")
    title_field.send_keys('Do grocery shopping')
    title_field.submit()
    wait.until(EC.visibility_of_element_located((By.ID, 'not-started-1')))

    todo_table = driver.find_element_by_id("not-started")

    assert 'Do grocery shopping' in todo_table.text

    delete_btn = driver.find_element_by_id("delete-todo-1")
    delete_btn.click()
    wait.until(EC.alert_is_present())

    driver.switch_to.alert.accept()
    wait.until(EC.invisibility_of_element_located((By.ID, 'not-started-1')))

    todo_table = driver.find_element_by_id("not-started")
    assert 'Do grocery shopping' not in todo_table.text
