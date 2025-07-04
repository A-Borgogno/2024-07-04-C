from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(year(`datetime`)) as year
                        from sighting s
                        order by year desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(shape) as shape
                        from sighting s
                        where shape != ""
                        order by shape"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s 
                        where s.shape = %s 
                        and year(s.`datetime`) = %s"""
            cursor.execute(query, (shape, year))

            for row in cursor:
                result.append(Sighting(**row))

            cursor.close()
            cnx.close()
        return result