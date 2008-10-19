import postrank

p = postrank.PostRank()

print "TESTING 'feed_id'"
r = p('feed_id', appkey='newthink.net', format='json', url='http://newthink.net') 
print r[postrank.PROCESSED]['feed_id']

print "TESTING 'top_posts'"
p('top_posts', appkey='newthink.net', format='json', feed_id=76885, period='year', num=5)

print "TESTING 'postrank'"
f = p('postrank', appkey='newthink.net', format='json', urls=['http://www.igvita.com/2008/06/19/splunk-your-distributed-logs-in-ec2/','http://www.igvita.com/2008/02/11/nginx-and-memcached-a-400-boost/','http://newthink.net/blog/2007/10/01/what-is-this-rails-thing/'])
print f[0]

print "TESTING 'feed'"
p('feed', appkey='newthink.net', format='json', feed_id=76885, level='best', num=3)


#from httplib import HTTPConnection

#c = HTTPConnection("api.postrank.com")
#c.request("POST", "/v1/postrank?appkey=aiderss.com&format=json", "url[]=http://www.igvita.com/2008/06/19/splunk-your-distributed-logs-in-ec2/&url[]=http://www.igvita.com/2008/02/11/nginx-and-memcached-a-400-boost/&")
#r = c.getresponse()
#print r.read()
