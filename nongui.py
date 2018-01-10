import sys
from postscraper import PostScraper

database = "PostScraping"

with open("config.txt") as file:
    clientData = [file.readline().strip("\n") for x in range(5)]
    desired = " ".split(file.readline().strip("\n"))
    index = file.readline().strip("\n")

if len(sys.argv) < 6:
    print("Incorrect syntax, correct usage:")
    print("nongui.py subreddit (new|hot|top) limit period")
    sys.exit()

subr = sys.argv[1]
orgby = sys.argv[2]
limit = sys.argv[3]
period = sys.argv[4]
cycles = int(sys.argv[5])
if period[-1:] == "m":
    period = int(period[:-1]) * 60
else:
    period = int(period)

desired = ["fullname", "title", "url", "permalink", "subreddit", "created", "over_18", "score"]
tables = ["after" + str(x * period) for x in range(cycles+1)]

pscraper = PostScraper(database, clientData, tables, desired, index)
pscraper.startScraping(period, subr, orgby, limit)