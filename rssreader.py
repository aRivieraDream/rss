import feedparser, time, csv

feed_file = 'rssList.csv'
out_file = 'rssStoryLinks.csv'

#takes a name of an output file and either opens it or creates a new file
#and opens that
def get_output(out_file):
	try:
		output = open(out_file, 'a')
	except Exception, e:
		import os
		#if you can't open the file assume it's because it doesn't exist
		#and make a new one. 
		output = os.mkdir(out_file)
	return output	


#takes an empty list and fills it with items from csv
def get_feeds(feed_file):
	data = []
	with open(feed_file, 'rU') as csvfile:
		feedReader = csv.reader(csvfile, delimiter=",", quotechar='"',
			dialect=csv.excel_tab) #needs all this shit to parse csv
		for row in feedReader:
			data.append(row)
	return data

#takes a link to an rss and a timestamp of the last update and creates a list
#of all new links pulled from that feed after the input timestamp
def new_entries(feed, timestamp):
	new_links = []
	feed = feedparser.parse(feed)
	feed.sort() #sorts into cronological order 
	feed.reverse() #last entry first
	for entry in feed['entries']:
		story_link = entry['link']
		published = entry['published']
		if published > timestamp:
			new_links.append(story_link)
	return new_links

#takes a list of links and an open output file to print to
"""
Have to update the timestamp in the feed file list
"""
def write_new(story_links, output):
	for story in story_links:
		output.append(story + '\n')

#takes a string as a time and converts it to a time object
def convert_time(last_entry):
	timestamp = time.strptime(last_entry, '%a, %b %d %H:%M:%S %Y +0000')
	return timestamp


#2xn list where the left element is the feed url and the right element is the last
#updated time.
feed_list = get_feeds()
output = get_output()

for feed in feed_list:
	feed_url = feed[0]
	last_entry = feed[1]
	last_entry = convert_time(last_entry)
	story_links = new_entries(feed_url, last_entry)
	write(story_links, output)
	

