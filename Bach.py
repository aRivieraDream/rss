# Takes crawler data from RTS and creates an RSS feed.
#TODO Use flask to publish feed
#TODO Store time of most recent post for referencing in query
import pymssql

# query for sql
def query():
    return """
    select top 50
        t.entityid
        , t.name
        , t.createdat
        , t.roundamount
        , t.existinrts
        , tf.[file] as [file]
        , tf.size
    from task t
        inner join taskfile tf on tf.taskid = t.entityid
    where t.type in (1, 2, 13, 14) --form d
     order by t.createdat desc
    """

# prep creds and create cursor
def get_cursor():
    server = 'replica.pitchbookdata.com'
    user = 'pierce.young'
    creds = 'fas44aca'
    db = 'dbd'
    encode = 'UTF-8'
    conn = pymssql.connect(server=server, user=user, password=creds, database=db, charset=encode)
    cursor = conn.cursor()
    cursor.execute(query())
    return cursor

# create story from a row from query --Consider using a map to map indecies
def create_story(row):
    story = {'title':row[1], 'story':row[5], 'pubDate':row[2]}
    return story

# just keeping these here for external referencing, delete later
"""
server = 'replica.pitchbookdata.com'
user = 'pierce.young'
creds = 'fas44aca'
db = 'dbd'
encode = 'UTF-8'
conn = pymssql.connect(server=server, user=user, password=creds, database=db, charset=encode)
cursor = conn.cursor()
cursor.execute(query())
row = cursor.fetchone()
"""

if __name__ == "__main__":
    server = 'replica.pitchbookdata.com'
    user = 'pierce.young'
    creds = 'fas44aca'
    db = 'dbd'
    encode = 'UTF-8'
    conn = pymssql.connect(server=server, user=user, password=creds, database=db, charset=encode)
    cursor = conn.cursor()
    cursor.execute(query())
    row = cursor.fetchone()
