from DBController.DBConnection import DBConnection


class StudentInfoTable:
    def insert_a_student(self, name):
        command = "INSERT INTO student_info (name) VALUES  ('{}');".format(name)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_a_student(self, stu_id):
        command = "DELETE FROM student_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_a_student(self, stu_id, name):
        command = "UPDATE student_info SET name='{}' WHERE stu_id='{}';".format(name, stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_a_student(self, name):
        command = "SELECT * FROM student_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        try:
            return [row['stu_id'] for row in record_from_db][0]
        except Exception as e:
            return -1

    def select_all_student(self):
        command = "SELECT * FROM student_info;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        name_dict = {}
        for row in record_from_db:
            name_dict[row['stu_id']] = row['name']


        return name_dict