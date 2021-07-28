import requests 
from bs4 import BeautifulSoup
import pprint

# start and end pages for data extraction
start_page = 1
end_page = 5

# create empty lists
mega_links=[]
mega_subtext=[]

def sort_stories_by_votes(hnlist):
	# simple sort algorithm, using lambda function for key sort, highest first
	return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
	# create empty list
	hn = []
	# index links
	for idx, item in enumerate(links):
		# grab the title
		title = item.getText()
		# grab the links, default None for broken links etc.
		href = item.get('href', None)
		# grab the score (use index)
		vote = subtext[idx].select('.score')
		# only run if vote exists
		if len(vote):
			# grab the score as integer removing ' points'
			points = int(vote[0].getText().replace(' points', ''))
			# only care about scores of 100+
			if points > 99:
				# add dictionary to list
				hn.append({'title': title, 'link': href, 'votes': points})
	# sort list
	return sort_stories_by_votes(hn)

# go through each page to collect data
for page in range(start_page, end_page +1):
	# Hacker News news page
	url = 'https://news.ycombinator.com/news' + f'?p={page}'
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'html.parser')
	links = soup.select('.storylink')
	subtext = soup.select('.subtext')
	# add data to mega lists
	mega_links.extend(links)
	mega_subtext.extend(subtext)
	# clear page lists
	links.clear()
	subtext.clear()

# Pretty Print complete list
pprint.pprint(create_custom_hn(mega_links, mega_subtext))