from prawutils import PrawStream
import time

class PostScraper:
    def __init__(self, database, clientData, tables=["after0", "after30", "after60", "after90", "after120", "after150", "after180"], desired=False):
        if database[-3:] != ".db":
            self.database = database + ".db"
        else:
            self.database = database
        if desired == False:
            self.desired = ["fullname", "title", "url", "permalink", "subreddit", "created", "score"]
        else:
            self.desired = desired
        self.username = clientData[0]
        self.password = clientData[1]
        self.client = clientData[2]
        self.secret = clientData[3]
        self.useragent = clientData[4]
        
        self.tables = tables
        self.structure = self.createStructure(self.desired)
        
        self.connect()
        self.setupTables(self.structure, self.tables, True, True)
    
    def createStructure(self, desired):
        typedict = {"score" : "integer"}
        f = lambda x: [x, self.testForInDict(x, typedict, "text")]
        return [f(x) for x in desired]
    
    def connect(self):
        self.prawstream = PrawStream(self.database, self.client, self.secret, self.password, self.useragent, self.username)
        self.conn = self.prawstream.getConn()
        #print(self.prawstream)
    
    def testForInDict(self, key, dictionary, default):
        if key in dictionary:
            return dictionary[key]
        else:
            return default
    
    def setupTables(self, structure, names, overwrite=False, ifnotexists=False):
        c = lambda z: [["score" + str((x + 1) * 10), "text"] for x in range(z)]
        structures = [structure + c(x) for x in range(len(names))]
        for i in range(len(names)):
            self.conn.createTable(names[i], structures[i], ifnotexists=ifnotexists, overwrite=overwrite)
        self.conn.commit()
    
    def run(self, runs, subr, orgby, limit):
        print("Scraping " + str(limit) + " posts from " + subr + "/" + orgby)
        for i in reversed(range(runs)):
            self.prawstream.update(self.tables[i], self.tables[i+1], 0)
            self.conn.deleteTable(self.tables[i])
            self.prawstream.commit()
        self.prawstream.export(self.tables[0], subr, orgby, limit, self.desired)
        self.prawstream.commit()
        if runs < (len(self.tables) - 1):
            runs += 1
        return runs
    
    def startScraping(self, period, subr, orgby, limit):
        self.runs = 0
        while True:
            self.runs = self.run(self.runs, subr, orgby, limit)
            time.sleep(period)