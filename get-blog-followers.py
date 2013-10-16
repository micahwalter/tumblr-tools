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
	
	data = client.followers(sys.argv[1], offset=0, limit=1)
	print json.dumps(data, indent=4, sort_keys=True)
	num_followers = int(data['total_users'])
	
	for x in xrange(0, num_followers, 20):
		followers = client.followers(sys.argv[1], offset=x, limit=20)	
		for follower in followers['users']:
			print json.dumps(follower, indent=4, sort_keys=True)
			if opts.save == 'yes':
				filename = 'data/followers/' + 'follower-of-' + str(sys.argv[1]) + '-' + str(follower['name']) + '.json'
				f = open(filename, 'w')
				f.write(json.dumps(follower, indent=4, sort_keys=True))
				f.close()