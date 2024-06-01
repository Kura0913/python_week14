from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer
from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class PrintAllSrvStru():
    def __init__(self):
        pass

    def execute(self, parameters):
        DBConnection.db_file_path = "students_score_DB.db"
        DBInitializer().execute()

        stu_dict = {}
        reply_msg = {'status':''}
        stu_name_dict = StudentInfoTable().select_all_student()
        for stu_id, name in stu_name_dict.items():
            scores_dict = SubjectInfoTable().select_subjects(stu_id)
            stu_dict[name] = {'name':name, 'scores':scores_dict}
        if stu_dict != None:
            reply_msg['status'] = 'OK'
            reply_msg['parameters'] = stu_dict
        else:
            reply_msg['status'] = 'Fail'
            reply_msg['reason'] = 'Get students list fail.'
        
        return reply_msg