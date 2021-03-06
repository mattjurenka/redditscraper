import praw
from easysqlite import EasyConnection
#from requests import RequestException

class PrawStream():
    def __init__(self, database, client_id, client_secret, password, user_agent, username):
        self.client_id = client_id
        self.client_secret = client_secret
        self.password = password
        self.user_agent = user_agent
        self.username = username
        
        self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, password=self.password, user_agent=self.user_agent, username=self.username)
        #print(client_id, client_secret, password, user_agent, username)
        self.easyconn = EasyConnection(database)
        self.testsub = self.reddit.subreddit("all")
        self.easyconn.connect()
    
    def refresh(self):
        self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, password=self.password, user_agent=self.user_agent, username=self.username)
        print("Refreshed token")
    
    #returns set amount of posts from a subreddit
    def getPosts(self, subr, orgby, num, desired=False):
        self.refresh()
        orgby = orgby.lower()
        num = int(num)
        #print(subr, orgby, num, desired)
        subreddit = self.reddit.subreddit(subr)
        #print(subreddit)
        typedict = {"hot" : subreddit.hot(limit=num),
                    "new" : subreddit.new(limit=num),
                    "top" : subreddit.top(limit=num)}
        #print(typedict[orgby])
        postgen = typedict[orgby]
        postlist = list(postgen)
        #print(postlist)
        
        #returns list of defined desired attributes if arg is supplied
        if not (desired is False):
            altreturn = []
            for i in postlist:
                altreturn.append(self.extract(i, desired))
            postlist = altreturn
        
        return postlist
    
    #extracts desired attributes from submission object
    def extract(self, submission, desired):
        relevant = []
        vardict = vars(submission)
        for i in desired:
            #handles getting display name of subreddit
            if i == "fullname":
                relevant.append(submission.fullname)
            elif isinstance(vardict[i], type(self.testsub)):
                altvardict = vars(vardict[i])
                subname = altvardict["display_name"]
                relevant.append(subname)
            else:
                relevant.append(vardict[i])
        return relevant
    
    def getConn(self):
        return self.easyconn
    
    #Pipes results of getPosts into EasyConnection.insertInto
    def export(self, table, subr, orgby, num, desired=False):
        self.refresh()
        posts = self.getPosts(subr, orgby, num, desired)
        self.easyconn.insertIntoMany(table, posts)
        return True
    
    #handles errors when post is deleted
    def getScoreDict(self, submissionList):
        scoreDict = {}
        for i in submissionList:
            try:
                scoreDict[i.fullname] = vars(i)["score"]
            except:
                pass
        return scoreDict
                
    #inputs sql table and inserts those values into another table with an updated score
    def update(self, inittable, aftertable, index):
        rows = self.easyconn.select(inittable, "*")
        rowDict = {x[index] : x for x in rows}
        
        fullnames = list(rowDict.keys())
        submissions = list(self.reddit.info(fullnames))
        scoreDict = self.getScoreDict(submissions)
        
        updatedrows = [list(rowDict[x]) + [scoreDict[x]] for x in scoreDict.keys()]
        self.easyconn.insertIntoMany(aftertable, updatedrows)
        return True
    
    
    def commit(self):
        self.easyconn.commit()
        return True
