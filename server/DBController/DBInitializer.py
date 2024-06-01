from DBController.DBConnection import DBConnection


necessary_table_to_create = {
    "student_info":
        """
            CREATE TABLE student_info
            (
                stu_id INTEGER PRIMARY KEY,
                name VARCHAR(255)         
            );
        """,

    "subject_info":
        """
            CREATE TABLE subject_info
            (
                stu_id INTEGER,
                subject VARCHAR(255),
                score FLOAT
            );
        """
}


class DBInitializer:
    def execute(self):
        existing_tables = self.get_existing_tables()
        self.create_not_exist_table(existing_tables)

    def get_existing_tables(self):
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            records = cursor.fetchall()

        return [single_row["tbl_name"] for single_row in records]

    def create_not_exist_table(self, existing_tables):
        for necessary_table, table_creating_command in necessary_table_to_create.items():
            if necessary_table not in existing_tables:
                self.create_table_with_specefied_command(table_creating_command)

    def create_table_with_specefied_command(self, command):
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()