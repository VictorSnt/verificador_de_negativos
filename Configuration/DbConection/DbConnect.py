import psycopg2


class DbConnection:

    def __init__(self, host: str, port: str, dbname: str, user: str, password: str):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.error = None
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        try:

            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            self.conn = conn
            self.cursor = self.conn.cursor()
            self.error = None
            return self
        except psycopg2.Error as e:
            self.error = e
            return False

    def sqlquery(self, query, args=False, commit=False) -> list | bool:

        if not self.cursor:
            self.error = "Você não esta conectado em nenhum banco"
            return False
        else:
            
                
                if args:
                    self.cursor.execute(query, args)

                else:
                    self.cursor.execute(query)

                if commit:
                    return

                columns = [desc[0] for desc in self.cursor.description]
                rows = self.cursor.fetchall()
                results_list = [{column: value for column, value in zip(columns, row)} for row in rows]

                return results_list

            

    def closeconnection(self) -> bool:

        try:
            self.cursor.close()
            self.conn.close()
            self.error = None
            return True

        except psycopg2.Error as e:
            self.error = e
            return False
