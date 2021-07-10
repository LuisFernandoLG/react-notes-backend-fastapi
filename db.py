from dns.rdatatype import NULL
from mysql.connector import connect, Error

db_config = {
    "host": "remotemysql.com",
    "port": "3306",
    "user": "ZyweErwf9W",
    "password": "hM3UZlZ9R3",
    "database": "ZyweErwf9W"
}


class Note():
    def __init__(self, title, content, color, date):
        self.title = title
        self.content = content
        self.color = color
        self.date = date


class Db():
    def __init__(self, config):
        self.config = config
        self._connection = NULL
        self._cursor = NULL

    def get_connection(self):
        try:
            con = connect(host=self.config["host"], port=self.config["port"],
                          user=self.config["user"], passwd=self.config["password"], database=self.config["database"])
            self._connection = con
        except Error as e:
            print(e)

    def get_cursor(self):
        self._cursor = self._connection.cursor()

    def close_connections(self):
        self._connection.close()

    def get_connections(self):
        self.get_connection()
        self.get_cursor()

    def get_all(self):
        self.get_connections()

        self._cursor.execute("SELECT * FROM notes")
        results = self._cursor.fetchall()
        resultsFormated = self.transformToNote(results)

        self.close_connections()

        return resultsFormated

    def get(self, id):
        query = f"SELECT * FROM notes WHERE id={id}"
        self._cursor.execute(query)
        results = self._cursor.fetchall()
        return results

    def put(self, note):
        self.get_connections()

        query = f"INSERT INTO notes(title, content, color, date) VALUES('{note.title}', '{note.content}', '{note.color}', '{note.date}')"
        print(query)
        self._cursor.execute(query)
        self._connection.commit()

        self.close_connections()
        return "Ok!"

    def delete(self, id):
        self.get_connections()

        query = f"DELETE FROM notes WHERE id={id}"
        self._cursor.execute(query)
        self._connection.commit()

        self.close_connections()
        return "Ok!"

    def updateEntire(self, id, note: Note):
        self.get_connections()
        query = f"UPDATE notes SET title = '{note.title}', content = '{note.content}', color = '{note.color}', date = '{note.date}' WHERE id = {id}"

        print(query)
        self._cursor.execute(query)
        self._connection.commit()
        self.close_connections()
        return "Ok!"

    def update(self, id, name, value):
        query = f"UPDATE notes SET {name} = {value} WHERE id = {id}"
        self._cursor.execute(query)
        self._connection.commit()
        return "Ok!"

    def transformToNote(self, notes: list):
        notesFormated = []
        for note in notes:
            notesFormated.append({
                "id": note[0],
                "title": note[1],
                "content": note[2],
                "color": note[3],
                "date": note[4]
            })

        return notesFormated


# db = Db(db_config)
# db.get_connection()
# # db.get_all()
# # print(db.get(2))

# # note1 = Note("Third Note", "This is the content", "272727")
# # db.put(note1)
# # db.delete(4)

# note2 = Note("Title", "Holis Cambiado", "585858")
# db.update(1, note2)
