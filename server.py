from flask import Flask, request, jsonify

from sql_connection import get_sql_connection

app = Flask(__name__)

connection = get_sql_connection()


@app.route('/getPersonalDetails', methods=['GET'])
def get_personal_details():
    """
    This api will return all the personal details.

    Input 1 : Person Type - (Student, Librarian)

    Input 2 : Person Id - (student_id, librarian_id)

    Output : All Personal Details
    """
    # request_payload = json.loads(request.form['data'])
    # product_id = product_dao.update_product(connection, request_payload)
    response = jsonify({
        'product_id': "product_id"
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getBorrowList', methods=['GET'])
def get_borrow_list():
    """

    This api will return all the borrow list.

    Input 1 : (student_id)

    output : List of borrow_id with details
    """






@app.route('/getBorrowDetails', methods=['GET'])
def get_borrow_details():
    """
    This api will return all the borrow details.

    Input 1 : (borrow_id)

    Output : Borrow Details
    """



@app.route('/getBookList', methods=['GET'])
def get_book_list():
    """
    This api will return all the book list.

    Input 1 : book_name_prefix

    output : All books which has name with given prefix
    """

@app.route('/getBookDetails', methods=['GET'])
def get_book_details():
    """
    This api will return all the book details.

    Input 1 : book_id

    Output : Book Details
    """

@app.route('/lendBook', methods=['POST'])
def lend_book():
    """
    This api will generate the borrow id.

    Input 1 : borrow_time, student_id, borrow_period, book_id, liabrarian_id

    output : Borrow id with details
    """

@app.route('/returnBook', methods=['PUT'])
def return_book():
    """
    This api will give total fine.

    Input 1 : number_of_books, submiton_time, book_id, liabrarian_id, borrow_id

    output : return fine
    """


if __name__ == "__main__":
    print("starting python Flask server For Grocery Store Management System")
    app.run(port=5000)
    get_personal_details()