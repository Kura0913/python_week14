from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer
from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class QuerySrvStru():
    def __init__(self):
        pass

    def execute(self, parameters):
        DBConnection.db_file_path = "students_score_DB.db"
        DBInitializer().execute()

        reply_msg = {'status': ''}        
        
        stu_id = StudentInfoTable().select_a_student(parameters['name'])

        if stu_id > 0:
            reply_msg['status'] = 'OK'
            reply_msg['scores'] = SubjectInfoTable().select_subjects(stu_id)

        else:
            reply_msg['status'] = 'Fail'
            reply_msg['reason'] = 'The name is not found.'
            
        return reply_msg