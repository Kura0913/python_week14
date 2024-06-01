from DBController.DBConnection import DBConnection

class SubjectInfoTable:
    def insert_a_subject(self, stu_id, subject, score):
        command = f"INSERT INTO subject_info (stu_id,subject,score) VALUES  ('{stu_id}','{subject}','{score}');"
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_subjects(self, stu_id):
        command = f"SELECT * FROM subject_info WHERE stu_id='{stu_id}';"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        score = {}
        for row in record_from_db:
            score[row['subject']] = row['score']

        return score

    def delete_subjects(self, stu_id):
        command = f"DELETE FROM subject_info WHERE stu_id='{stu_id}';"
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_a_subject(self, stu_id, subject, score):
        command = f"UPDATE subject_info SET score='{score}' WHERE stu_id = '{stu_id}' AND subject = '{subject}';"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()