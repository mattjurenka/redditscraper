import sqlite3

class EasyConnection():
    def __init__(self, database):
        if database[-3:] != ".db":
            self.database = database + ".db"
        else:
            self.database = database
    
    #handles innitial database connection
    def connect(self):
        self.conn = sqlite3.connect(self.database)
        self.c = self.conn.cursor()
        return (self.conn, self.c)

    def close(self):
        self.conn.close()
        return True
    
    def commit(self):
        self.conn.commit()
        return True
    
    def getDatabase(self):
        return self.database

    #inserts a list of values into sql table
    def insertInto(self, table, values):
        cmd = "insert into %s values " % table
        prepared = "("
        for i in range(0, len(values)):
            prepared += "?, "
        prepared = prepared[:-2] + ")"
        cmd += prepared
        #print(cmd, values)
        self.c.execute(cmd, values)
        return True

    #inserts two dimensional array of values into sql table
    def insertIntoMany(self, table, values):
        for i in values:
            #print(i)
            self.insertInto(table, i)
        return True
    
    #creates sql table with given value list
    def createTable(self, name, structure, ifnotexists=False, overwrite=False):
        if overwrite == True:
            self.c.execute("drop table if exists " + name)
        
        cmd = "create table "
        if ifnotexists:
            cmd += "if not exists "
        cmd += "%s (" % name
        for i in range(0, len(structure)):
            cmd += " ".join(structure[i]) + ", "
        cmd = cmd[:-2] + ")"
        self.c.execute(cmd)
        return True
    
    #returns list of rows defiend by select arguments
    def select(self, table, args):
        self.c.execute("select " + args + " from " + table)
        rows = self.c.fetchall()
        return rows
    
    def deleteTable(self, table):
        self.c.execute("delete from " + table)
        return True
    
    def execute(self, cmd):
        self.c.execute(cmd)
        return True
    
    def close(self):
        self.conn.close()
        return True