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
	
	data = client.info()
	print json.dumps(data, indent=4, sort_keys=True)

	if opts.save == 'yes':
		filename = 'data/users/' + data['user']['name'] + '-info.json'
		f = open(filename, 'w')
		f.write(json.dumps(data, indent=4, sort_keys=True))
		f.close()