from server import connection
from sql_connection import get_sql_connection

def get_personal_details(Connection, student_id):
    print("getting personal details.....")


    cursor = Connection.cursor()
    query = ("select student_id, student_name, enrollment_no, department from student where student_id = %s")

    cursor.execute(query, (student_id))

    response = []

    for (student_id, student_name, enrollment_no, department) in cursor:
        response.append(
            {
            "student_id" : student_id,
            "student_name" : student_name,
            "enrollment_no" : enrollment_no,
            "department" : department

            }
        )
    return response
def get_borrow_list(Connection, student_id):
    print("getting borrow list.....")

    cursor = Connection.cursor()
    query = ("select Borrow_id, student_id, borrow_time, fine, liabrarian_id, borrow_period, number_of_books from borrow where student_id = %s")

    cursor.execute(query, (student_id,))
    response = []
    for (Borrow_id, student_id, borrow_time, fine, liabrarian_id, borrow_period, number_of_books) in cursor:
        response.append(
            {
            "Borrow_id" : Borrow_id,
            "student_id" : student_id,
             "borrow_time" : borrow_time,
             "fine" : fine,
             "liabrarian_id" : liabrarian_id,
             "borrow_period" : borrow_period,
             "number_of_books" : number_of_books

            }
        )
    return response
def get_borrow_details(Connection, Borrow_id):
    print("getting borrow details.....")
    cursor = Connection.cursor()
    query = ("select Borrow_id, Book_id, number_of_books, submission_time, liabrarian_id from borrow_detail where Borrow_id = %s")

    cursor.execute(query, (Borrow_id,))
    response = []

    for (Borrow_id, Book_id, number_of_books, submission_time, liabrarian_id) in cursor:
        response.append(
            {
            "Borrow_id" : Borrow_id,
            "Book_id" : Book_id,
            "number_of_books" : number_of_books,
            "submission_time" : submission_time.strftime("%Y-%m-%d"),
            "liabrarian_id" : liabrarian_id
            }
        )
    return response

def get_book_list(connection, prefix):
    print("getting books.....")
    cursor = connection.cursor()
    query = ("select Book_id, Book_name, subject, author_name, number_of_books from books where Book_name like %s")
    cursor.execute(query, (prefix,))
    response = []

    for (Book_id, Book_name, subject, author_name, number_of_books) in cursor:
        response.append(
            {
            "Book_id" : Book_id,
            "Book_name" : Book_name,
            "subject" : subject,
            "author_name" : author_name,
            "number_of_books" : number_of_books
            }
        )
    return response

def get_book_details(Connection, Book_id):
    print("getting book details.....")
    cursor = Connection.cursor()
    query = ("select Book_id, Book_name, subject, author_name, number_of_books from books where Book_id = %s")
    cursor.execute(query, (Book_id,))
    response = []
    for (Book_id, Book_name, subject, author_name, number_of_books) in cursor:
        response.append(
            {
            "Book_id" : Book_id,
            "Book_name" : Book_name,
            "subject" : subject,
            "author_name" : author_name,
            "number_of_books" : number_of_books

            }
        )
    return response

def add_books(connection, Book):
    cursor = connection.cursor()

    query = ("insert into books"
             "(Book_name, subject, author_name, number_of_books) values (%s, %s, %s, %s)")
    data = (Book['Book_name'], Book['subject'], Book['author_name'], Book['number_of_books'])
    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def lend_books(Connection, Book):
    cursor = Connection.cursor()

    query_1 = ("insert into borrow"
             "(student_id, borrow_time, fine, liabrarian_id, borrow_period, number_of_books) values (%s, %s, %s, %s, %s, %s)")
    data_1 = (Book['student_id'], Book['borrow_time'], Book['fine'], Book['liabrarian_id'], Book['borrow_period'], Book['number_of_books'])
    cursor.execute(query_1, data_1)
    connection.commit()

    Borrow_id = cursor.lastrowid

    query_2 = ("insert into borrow_detail"
               "(Borrow_id, Book_id)" 
               "values (%s, %s)")
    data_2 = []

    for Book_id in Book['book_list']:
        data_2.append([
            Borrow_id, Book_id
        ])

    cursor.executemany(query_2, data_2)
    connection.commit()
    return Borrow_id

def submit_book(Connection, Book_id, Borrow_id,):
    cursor = Connection.cursor()

    query_1 = ("select number_of_books from books where Book_id = %s")
    data_1 = (Book_id,)
    cursor.execute(query_1, data_1)

    no_of_books = cursor.fetchone()[0] + 1
    # no_of_books = no_of_books + 1

    query_2 = ("update liabrary.books set number_of_books = %s where Book_id = %s")
    data_2 = (no_of_books, Book_id,)
    cursor.execute(query_2, data_2)


    query_3 = ("select borrow_time, borrow_period, student_id from borrow where Borrow_id = %s")
    data_3 = (Borrow_id,)
    cursor.execute(query_3, data_3)

    rows = cursor.fetchone()



    date_2 = rows[0]
    period = rows[1]
    studentId = rows[2]

    from datetime import date
    date1 = date.today()

    difference = date_2 - date1

    if difference.days > period:
        fine_1 = (difference.days - period)*2
    else:
        fine_1 = 0

    query_4 = ("select fine from borrow where Borrow_id = %s")
    data_4 = (Borrow_id,)
    cursor.execute(query_4, data_4)

    fine_2 = cursor.fetchone()[0] + fine_1

    query_5 = ("update liabrary.borrow set fine = %s where Borrow_id = %s")
    data_5 = (fine_2,Borrow_id,)
    cursor.execute(query_5, data_5)


    query_6 = ("update liabrary.student  set fine = %s where student_id = %s")
    data_6 = (fine_2,studentId,)
    cursor.execute(query_6, data_6)


    query_7 = ("update liabrary.borrow_detail set submission_time = %s where Borrow_id = %s and Book_id = %s ")
    data_7 = ("2026-01-26", Borrow_id,Book_id, )
    cursor.execute(query_7, data_7)
    connection.commit()

    return no_of_books


def test():
    nums = [4, 5, 6, 7, 0, 1, 2]
    target = 0

    n = len(nums)
    i = 0
    x = n - 1
    if nums[i] == target:
        return i
    if nums[x] == target:
        return x
    while i < n:
        mid = (i + x) // 2
        print(mid, nums[mid])
        if target == nums[mid]:
            return mid
        if nums[mid] > nums[i]:
            if target < nums[mid] and target > nums[i]:
                x = mid
            else:
                i = mid
        else:
            if target > nums[mid] and target < nums[x]:
                i = mid
            else:
                x = mid
    return -1


if __name__ == "__main__":

    # print(test())
    #
    # Connection = get_sql_connection()
    # # print(get_personal_details(Connection,3))
    # print(get_borrow_list(Connection, 1))
    # print(get_borrow_details(Connection, 1))
    # print(get_book_list(Connection, "the%"))
    # print(get_book_details(Connection, 1))
    # print(add_books(Connection, {
    #     'Book_name': 'fluidMechanics',
    #     'subject': 'Mechanics',
    #     'author_name': 'CMjha',
    #     'number_of_books': 2
    #     }
    # ))
    # print (insert_submit_books(Connection, {
    #     "submission_time" : "2026-1-19",
    #     }
    # ))
    # print(lend_books(Connection, {
    #     "student_id" : 2,
    #     "borrow_time" : "2026-1-24",
    #     "fine" : 0,
    #     "liabrarian_id" : 1,
    #     "borrow_period" : 9,
    #     "number_of_books" : 3,
    #     "book_list" : [1, 2, 3]
    # }
    # ))
    # print(submit_book(Connection, 1 , 15))

    import numpy as np
# x = np.array([4, 5, 6, 7, 0, 1, 2])
# # print(x)
# # print(type(x))
# ar_zero = np.zeros(4)
# ar_zero1 = np.zeros((3,4))
# ar_ones = np.ones(4)
# ar_em = np.empty(4)
# ar_rn = np.arange(4)
# ar_dia = np.eye(3,5 )
# ar_lin = np.linspace(0, 10, num = 5)
# var = np.random.rand(4)
# var1 = np.random.rand(3,4)
# var2 = np.random.randn(2,4)
# var3 = np.random.ranf(4)
# var4 = np.random.randint(3,8, 2)
# x1 = np.array([2.3, 5.6, 9.3])
# x2 = np.array(["tor", "oql","pot"])
# x3 = np.array(["r", "u", "i"])
# x4 = np.array(["e","u",1,2,3])
# y = np.array([1,2,3,4,5] ,dtype = np.int8)
# y1 = np.array([1,2,3,4,5], dtype = "f")
# y2 = np.array([1,2,3,4,5])
# new = np.float32(y2)
# new1 = np.int_(new)
# # print("data type :" , y2.dtype)
# # print("data type :" , new.dtype)
# # print("data type :" , new1.dtype)
# y3 = np.array([1,2,3,4,5])
# y3_new = y3.astype(float)
# # print(y3)
# # print(y3_new)
# # car1 = np.array([3, 4 , 6, 7])
# # car2 = np.array([6, 0, 5, 3])
# # caradd = car1 + car2
# # carsub = car1 - 6
# # carmul = car1 * 6
# # cardiv = car1 / 4
# # carmod = car1 % 4
# #
# # print(carmod)
# #
# ans1 = np.array([5,6,7,8,9])
# # ans2 = np.array([1,2,3,4,5])
# #
# # ansadd = np.add(ans1,ans2)
# # print(ansadd)
# # var21 = np.array([[1,2,3,4,5],[6,7,8,9,10]])
# # var22 = np.array([[3,6,9,12,15],[5,10,15,20,25]])
# # varadd = var21 * var22
# # # print(varadd)
#
# # print(np.reciprocal(ans1))
# # print("max:" , np.max(ans1),np.argmax(ans1))
# print("min:" , np.min(ans1),np.argmin(ans1))
# var1 = np.array([[1,2,3,4],[3,6,9,5]])
# print(np.max(var1,axis = 0))
# var2 = np.array([4, 5, 6, 7, 0, 1, 2])
# # print(np.sqrt(var2))
# print(np.sin(var2))
# print(np.cos(var2))
# print(np.cumsum(var2))
# var = np.array([[1,4,7],[2,5,6]])
# print(var)
# print(var.shape)
# var1 = np.array([1,4,7,6], ndmin = 4)
# print(var1)
# print(np.ndim(var1))
# print(var1.shape)
# var2 = np.array([1,2,3,4,5,6])
# x = var2.reshape(3,2)
# x1 = x.reshape(-1)
# print(x)
# print(x1)
# print(x.ndim)
# print(var2.ndim)
# var1 = np.array([1, 2, 3])
# print(var1.shape)
# print(var1)
# var2 = np.array([[1],[2],[3]])
# print(var2.shape)
# print(var2)
# varadd = var1 + var2
# print(varadd)
# var1 = np.array([[1,2],[3,4]])
# print(var1)
# print(var1.ndim)
# print(var1[0,1])
# print(var1[0])
# var2 = np.array([[[1,2],[6,7]]])
# print(var2)
# print(var2.ndim)
# print()
# print(var2[0 ,1, 1])
# print(var2[2:5])
# print(var2[2:])
# print(var2[:5])
# print(var2[::2])
# print(var2[1:6:2])
# print(var1[0,0:])
# x = np.array([9,8,7,6,5,4,3,2,1])
# for i in x:
#     print(i)
# var = np.array([[1,2,3,4,5],[6,7,8,9,10]])
# for j in var:
#     for k in j:
#         print(k)
# var = np.array([[[9,8,7,6],[1,2,3,4]]])
# print(var)
# print(var.ndim)
# print()
# for i in np.nditer(var, flags = ['buffered'],op_dtypes=["S"]):
#     print(i)

# for i,j in np.ndenumerate(var):
#     print(i,j)
# co = var.copy()
# print(var)
# print(co)
# vi = var.view()
# print(vi)
# var1 = np.array([1,2,3,4])
# co = var1.copy()
# var1[1] = 40
# print("var :" ,var1)
# print("copy :", co)
#
# var2 = np.array([9,8,7,6])
# vi = var2.view()
# var2[2] = 60
#
# print("var2 :",var2)
# print("vi :",vi)
# var = np.array([[1,2],[3,4]])
# var1 = np.array([[9,8],[7,6]])
# ar = np.concatenate((var,var1), axis=0)
# print(var)
# print()
# print(var1)
# print()
# print(ar)
# a_new = np.stack((var,var1), axis = 1)
# print(a_new)
# a_new = np.dstack((var,var1))    h = along row ,v = column , d = along height
# print(a_new)
# var = np.array([1,2,3,4,5,6,10,11,12])
# # ar = np.array_split(var,3)
# print(var)
# print()
# print(ar)
# print()
# print(type(ar))
# var1 = np.array([[1,2],[3,4],[5,6]])
# ar1 = np.array_split(var1, 3)
# ar2 = np.array_split(var1, 3, axis=1)
# ar3 = np.array_split(var1, 3, axis=0)
# print(ar1)
# print()
# print(ar2)
# print()
# print(ar3)
# x = np.where(var == 2)
# x2 = np.searchsorted(var,7)
# x1 = np.searchsorted(var, [7,8,9], side = "right")
# print(x1)
# var1 = np.array([15,12,11,7,8,9])
# print(np.sort(var1))
# var2 = np.array(["q","a","b","c"])
# print(np.sort(var2))
# ans = np.array([[6,7],[3,2]])
# print(np.sort(ans))
# f = [True, False, True, False, True, False]
# new_a = var1[f]
# print(new_a)
# np.random.shuffle(var1)
# print(var1)
# var2 = np.array([2,3,2,5,4,3,8,9,5,3])
# print(np.unique(var2,return_index = True, return_counts = True))
# var = np.array([1,2,3,4,5,6])
# x = np.resize(var,(3,2))
# print(x)
# varry = np.array([1,2,3,4,5])
# y = np.resize(varry,(3,2))
# print(y)
# print(y.flatten(order="F"))
# print(y.flatten(order="C"))
# print(np.ravel(y, order="F"))
# ravel and flaten convert in single dimension  but by giving order
# resize can change single dimension in two dimension
var = np.array([1,2,3,4])
print(var)
v = np.insert(var , (2,4) ,40)
print(v)





















