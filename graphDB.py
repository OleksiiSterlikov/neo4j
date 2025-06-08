from neo4j import GraphDatabase


class Neo4jConnection:
    '''
    The Class cteate connection with Database 
    '''
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri=uri, auth=(user, password))

    def close(self):
        '''
        The Method closing sessions with Database
        '''
        if self.driver is not None:
            self.driver.close()

    def query(self, query, db=None):
        '''
        This Method send a request to the Database
        '''
        assert self.driver is not None, "Driver not initialazed!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as ex:
            print("Query failed:", ex)
        finally:
            if session is not None:
                session.close()
        return response
