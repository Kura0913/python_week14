from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer
from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class ModifySrvStru():
    def __init__(self):
        pass

    def execute(self, parameters):
        DBConnection.db_file_path = "students_score_DB.db"
        DBInitializer().execute()

        reply_msg = {'status': ''}

        stu_id = StudentInfoTable().select_a_student(parameters['name'])
        current_scores = SubjectInfoTable().select_subjects(stu_id)

        for subject, score in parameters['scores'].items():
            if subject in current_scores.keys():
                SubjectInfoTable().update_a_subject(stu_id, subject, score)
            else:
                SubjectInfoTable().insert_a_subject(stu_id, subject, score)

        reply_msg['status'] = 'OK'

        return reply_msg