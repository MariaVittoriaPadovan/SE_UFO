from database.DB_connect import DBConnect
from model.sighting import Sighting
from model.state import State
class DAO:

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM state"""

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(State(**row))

        except Exception as e:
            print("Errore durante la query state")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result # lista di oggetti stato

    @staticmethod
    def get_all_sighting():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT *
                FROM sighting
                ORDER BY s_datetime ASC
                """
        #ORDER BY s_datetime ASC mi permette di ordinare gli avvistamenti secondo l'anno in modo crescente
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(Sighting(**row))

        except Exception as e:
            print("Errore durante la query sighting")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di oggetti sighting

    @staticmethod
    def get_all_shapes():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT DISTINCT shape
                FROM sighting
                WHERE shape != ""
                """

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row['shape'])

        except Exception as e:
            print("Errore durante la query shape")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di shapes

    @staticmethod
    def get_all_weighted_neigh(year, shape):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT LEAST(n.state1, n.state2) AS st1,
                           GREATEST(n.state1, n.state2) AS st2, 
                           COUNT(*) as N
                    FROM sighting s , neighbor n 
                    WHERE year(s.s_datetime) = %s
                          AND s.shape = %s
                          AND (s.state = n.state1 OR s.state = n.state2)
                    GROUP BY st1 , st2 
                """

        try:
            cursor.execute(query, (year, shape))
            for row in cursor:
                result.append((row['st1'], row['st2'], row['N']))

        except Exception as e:
            print("Errore durante la query peso e archi")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di (stato di partenza, stato di arrivo, numero di avvistamenti in quell'anno di quella forma tra quei due stati)
