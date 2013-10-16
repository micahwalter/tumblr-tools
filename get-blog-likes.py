import sys
import os
import pytumblr
import json
import optparse


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
	
	data = client.blog_likes(sys.argv[1], offset=0, limit=1)
	print json.dumps(data, indent=4, sort_keys=True)
	num_likes = int(data['liked_count'])
	
	for x in xrange(0, num_likes, 20):
		likes = client.blog_likes(sys.argv[1], offset=x, limit=20)	
		for like in likes['liked_posts']:
			print json.dumps(like, indent=4, sort_keys=True)
			if opts.save == 'yes':
				filename = 'data/likes/' + str(sys.argv[1]) + '-liked-post-' + str(like['id']) + '.json'
				f = open(filename, 'w')
				f.write(json.dumps(like, indent=4, sort_keys=True))
				f.close()