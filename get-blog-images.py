import sys
import os
import pytumblr
import json
import optparse
import urllib

client = pytumblr.TumblrRestClient(
    os.environ['TUMBLR_CONSUMER_KEY'],
	os.environ['TUMBLR_CONSUMER_SECRET'],
	os.environ['TUMBLR_OAUTH_KEY'],
	os.environ['TUMBLR_OAUTH_SECRET'],
)


if __name__ == '__main__':

	parser = optparse.OptionParser()
	parser.add_option('-s', '--save', dest='save', action='store', help='save the api output to disk')

	(opts, args) = parser.parse_args()
	
	data = client.posts(sys.argv[1], offset=0, limit=1)
	num_posts = int(data['blog']['posts'])
	
	for x in xrange(0, num_posts, 20):
		posts = client.posts(sys.argv[1], offset=x, limit=20)	
		for post in posts['posts']:
			try:
				for photo in post['photos']:
					if opts.save == 'yes':
						url = photo['original_size']['url']
						filename = 'data/images/' + str(post['id']) + "-" + str(url.rsplit('/',1)[1])
						print filename
						urllib.urlretrieve(url, filename)
			except Exception, e:
				print "no photos :("

			
			
		