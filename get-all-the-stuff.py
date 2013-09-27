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
	
	### get user info
	user = client.info()
	print json.dumps(user, indent=4, sort_keys=True)

	if opts.save == 'yes':
		if not os.path.exists('data/users'):
		    os.makedirs('data/users')
		filename = 'data/users/' + user['user']['name'] + '-info.json'
		f = open(filename, 'w')
		f.write(json.dumps(user, indent=4, sort_keys=True))
		f.close()
	
	### TODO: get blogs the user is following
	
	### TODO: get posts the user has liked
	
	### start the looping
	### get all the blogs
	for blog in user['user']['blogs']:	
		info = client.blog_info(blog['name'])
		print json.dumps(info, indent=4, sort_keys=True)

		if opts.save == 'yes':
			if not os.path.exists('data/blogs'):
			    os.makedirs('data/blogs')
			filename = 'data/blogs/' + 'blog-' + str(blog['name']) + '-info.json'
			f = open(filename, 'w')
			f.write(json.dumps(info, indent=4, sort_keys=True))
			f.close()
		
		### get all the posts
		posts = client.posts(blog['name'], offset=0, limit=1)
		try:
			num_posts = int(posts['blog']['posts'])
		except Exception, e:
			print "no posts :("
		else:
			for x in xrange(0, num_posts, 20):
				posts = client.posts(blog['name'], offset=x, limit=20)	
				for post in posts['posts']:
					print json.dumps(post, indent=4, sort_keys=True)
					if opts.save == 'yes':
						if not os.path.exists('data/posts'):
						    os.makedirs('data/posts')
						filename = 'data/posts/' + 'post-' + str(post['id']) + '.json'
						f = open(filename, 'w')
						f.write(json.dumps(post, indent=4, sort_keys=True))
						f.close()
					try:
						for photo in post['photos']:
							if opts.save == 'yes':
								if not os.path.exists('data/images'):
								    os.makedirs('data/images')
								url = photo['original_size']['url']
								filename = 'data/images/' + str(post['id']) + "-" + str(url.rsplit('/',1)[1])
								print filename
								urllib.urlretrieve(url, filename)
					except Exception, e:
						print "no photos :("
					
					
		### get all the blogs's followers
		followers = client.followers(blog['name'], offset=0, limit=1)
		try:
			num_followers = int(followers['total_users'])
		except Exception, e:
			print "no followers :("
		else:
			for x in xrange(0, num_followers, 20):
				followers = client.followers(blog['name'], offset=x, limit=20)	
				for follower in followers['users']:
					print json.dumps(follower, indent=4, sort_keys=True)
					if opts.save == 'yes':
						if not os.path.exists('data/followers'):
						    os.makedirs('data/followers')	
						filename = 'data/followers/' + 'follower-of-' + str(blog['name']) + '-' + str(follower['name']) + '.json'
						f = open(filename, 'w')
						f.write(json.dumps(follower, indent=4, sort_keys=True))
						f.close()
							
		### get all the blog's likes
		likes = client.blog_likes(blog['name'], offset=0, limit=1)
		try:
			num_likes = int(likes['liked_count'])
		except Exception, e:
			print "no likes :("
		else:
			for x in xrange(0, num_likes, 20):
				likes = client.blog_likes(blog['name'], offset=x, limit=20)	
				for like in likes['liked_posts']:
					print json.dumps(like, indent=4, sort_keys=True)
					if opts.save == 'yes':
						if not os.path.exists('data/likes'):
						    os.makedirs('data/likes')
						filename = 'data/likes/' + str(blog['name']) + '-liked-post-' + str(like['id']) + '.json'
						f = open(filename, 'w')
						f.write(json.dumps(like, indent=4, sort_keys=True))
						f.close()

		### TODO: get all the things in the blog's queue
		
		### TODO: get all the blog's drafts
		
		### TODO: get all the blog's submissions