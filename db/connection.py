import mysql.connector

class DataBase:
    def __init__(self):
        self.__connection = None
        self.__curser = None
        self.__database = 'TicketSystem'

    def openConnection(self):
        self.__connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database=self.__database
        )
        self.__curser = self.__connection.cursor()

    def saveAndClose(self):
        self.__connection.commit()
        self.__connection.close()
        print('MySQL connection closed')

    def get_tickets_by_customer(self, customer_id):
        self.openConnection()
        sql = "SELECT * FROM T_Ticket WHERE CustomerId=%s ORDER BY CreatedAt DESC"
        self.__curser.execute(sql, (customer_id,))
        result = self.__curser.fetchall()
        self.saveAndClose()
        return result

    def get_tickets_by_priority(self, priority):
        if priority is None:
            sql = "SELECT * FROM T_Ticket WHERE Priorität IS NULL ORDER BY CreatedAt DESC"
            self.openConnection()
            self.__curser.execute(sql)
            result = self.__curser.fetchall()
            self.saveAndClose()
            return result
        else:
            sql = "SELECT * FROM T_Ticket WHERE Priorität=%s ORDER BY UpdatedAt DESC"
            self.openConnection()
            self.__curser.execute(sql, (priority,))
            result = self.__curser.fetchall()
            self.saveAndClose()
            return result

    def add_ticket(self, ticket):

        if self.__connection is None or self.__curser is None:
            self.openConnection()

        sql = """
            INSERT INTO T_Ticket
            (CustomerId, Thema, Beschreibung, Status, Firma, CreatedAt)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            ticket.customer_id,
            ticket.thema,
            ticket.beschreibung,
            ticket.status,
            ticket.firma,
            ticket.created_at
        )

        self.__curser.execute(sql, values)
        self.saveAndClose()

    def get_ticket_by_id(self, ticket_id):
        self.openConnection()
        sql = "SELECT * FROM T_Ticket WHERE ID=%s"
        self.__curser.execute(sql, (ticket_id,))
        result = self.__curser.fetchone()
        self.saveAndClose()
        return result

    def get_customer_by_id(self, customer_id):
        self.openConnection()
        sql = "SELECT * FROM T_Customer WHERE ID=%s"
        self.__curser.execute(sql, (customer_id,))
        result = self.__curser.fetchone()
        self.saveAndClose()
        return result