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


# Connection and create Database
connection = Neo4jConnection(uri='neo4j://localhost:7687', user='neo4j', password='Your-Password')
# connection.query("CREATE DATABASE graphdb IF NOT EXISTS")

# Import .csv tables to the database
QUERY_STRING = '''
LOAD CSV WITH HEADERS FROM 'file:///Teachers.csv' AS line FIELDTERMINATOR ','
MERGE (Teachers:Teachers {TeacherID: line.TeacherID})
 ON CREATE SET Teachers.LastName = line.LastName, Teachers.FirstName = line.FirstName, Teachers.SubjectID = line.SubjectID;
'''
connection.query(QUERY_STRING, db='neo4j')

QUERY_STRING = '''
LOAD CSV WITH HEADERS FROM 'file:///Students.csv' AS line FIELDTERMINATOR ','
MERGE (Students:Students {StudentID: line.StudentID})
 ON CREATE SET Students.LastName = line.LastName, Students.FirstName = line.FirstName;
'''
connection.query(QUERY_STRING, db='neo4j')

QUERY_STRING = '''
LOAD CSV WITH HEADERS FROM 'file:///Grades.csv' AS line FIELDTERMINATOR ','
MERGE (Grades:Grades {GradeID: line.GradeID})
 ON CREATE SET Grades.StudentID = line.StudentID, Grades.TeacherID = line.TeacherID, Grades.Grade = line.Grade;
'''
connection.query(QUERY_STRING, db='neo4j')

QUERY_STRING = '''
LOAD CSV WITH HEADERS FROM 'file:///Subjects.csv' AS line FIELDTERMINATOR ','
MERGE (Subjects:Subjects {SubjectID: line.SubjectID})
 ON CREATE SET Subjects.Name = line.Name;
'''
connection.query(QUERY_STRING, db='neo4j')

# Creating relationships between tables

QUERY_STRING = '''
LOAD CSV WITH HEADERS FROM 'file:///Grades.csv' AS line
MATCH (Grades:Grades {GradeID: line.GradeID})
MATCH (Students:Students {StudentID: line.StudentID})
CREATE (Students)-[:SOLD]->(Grades);
'''
connection.query(QUERY_STRING, db='neo4j')

QUERY_STRING = '''
LOAD CSV WITH HEADERS FROM 'file:///Grades.csv' AS line
MATCH (Grades:Grades {GradeID: line.GradeID})
MATCH (Teachers:Teachers {TeacherID: line.TeacherID})
CREATE (Teachers)-[:SOLD]->(Grades);
'''
connection.query(QUERY_STRING, db='neo4j')

QUERY_STRING = '''
LOAD CSV WITH HEADERS FROM 'file:///Teachers.csv' AS line
MATCH (Teachers:Teachers {TeacherID: line.TeacherID})
MATCH (Subjects:Subjects {SubjectID: line.SubjectID})
CREATE (Subjects)-[:SOLD]->(Teachers);
'''
connection.query(QUERY_STRING, db='neo4j')
