import sys
from postscraper import PostScraper

database = "PostScraping"

with open("credentials.txt") as file:
    clientData = [f.readline().strip("\n") for x in range(5)]

if len(sys.argv) < 5:
    print("Incorrect syntax, correct usage:")
    print("nongui.py subreddit (new|hot|top) limit period")
    sys.exit()

subr = sys.argv[1]
orgby = sys.argv[2]
limit = sys.argv[3]
period = sys.argv[4]
if period[-1:] == "m":
    period = int(period[:-1]) * 60
else:
    period = int(period)

desired = ["fullname", "title", "url", "permalink", "subreddit", "created", "over_18", "score"]
tables = ["after" + str(x * 30)  for x in range(13)]

pscraper = PostScraper(database, clientData, tables, desired)
pscraper.startScraping(period, subr, orgby, limit)