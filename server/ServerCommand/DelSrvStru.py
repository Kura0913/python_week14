from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer
from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class DelSrvStru():
    def __init__(self):
        pass

    def execute(self, parameters):
        reply_msg = {'status': ''}

        DBConnection.db_file_path = "students_score_DB.db"
        DBInitializer().execute()
        
        stu_id = StudentInfoTable().select_a_student(parameters['name'])

        SubjectInfoTable().delete_subjects(stu_id)
        StudentInfoTable().delete_a_student(stu_id)
        reply_msg['status'] = 'OK'

        return reply_msg