from urllib import urlencode

import httplib

DEFAULT_VER = "v1"
POSTRANK_URL = "api.postrank.com"

RAW = 0
PROCESSED = 1

class PostRank(object):
    def __init__(self, version=DEFAULT_VER):
        """
        Create a new PostRank object.
        
        'version' version of the api to use. Maps to the api url.
                  eg. http://api.postrank.com/<version>/postrank
        """
        self.version = version


    def __call__(self, resource, **kwargs):
        """ 
        Call to the PostRank api.

        Use the options outlined at http://postrank.com/api

        'resource' the api resource you want to use (feed_id, feed, postrank, etc).
        '**kwargs' api fields as per the api document.
        
        eg. 
            postrank = PostRank()
            result = postrank('feed_id', appkey='<your api key>', format='json', url='http://www.postrank.com')

        Note:
            When using the 'postrank' resource 
                - url[] is entered as an array of urls
                - feed_id[] is entered as an array of feed_id
        """
        method="GET"

        # unfortunatly, no standard uri change other than this to denote requirement of POST
        if (self.version == 'v1' and resource.endswith('postrank')):
            method='POST'
            postrank_urls = []
            postrankfeed_ids = []
            # get post args
            if kwargs.has_key('url'):
                for url in kwargs.pop('url'):
                    postrank_urls.append(url)
            if kwargs.has_key('feed_id'):
                for feed_id in kwargs.pop('feed_id'):
                    postrankfeed_ids.append(feed_id)
        
        if kwargs:
            # build api args
            args = urlencode(kwargs.items())    

        c = httplib.HTTPConnection(POSTRANK_URL)
        uri = "/%s/%s?%s" %(self.version, resource,args)

        try:
            if (method == "POST"):
                postargs = "%s&%s" %(urlencode({'url[]': postrank_urls}, True), urlencode({'feed_id[]': postrankfeed_ids}, True))
                c.request(method, "%s" %(uri), postargs)
            else:
                c.request(method, "%s" %(uri))
            result = c.getresponse()
        
            retVal = []

            if (result.status != 200):    # HTTP 200
                retVal.insert(RAW, None)
                retVal.insert(PROCESSED, None)
                return retVal

            retVal.insert(RAW, result.read())
            # process the raw input in the format specified
            if (kwargs['format'] == "json"):
                try:
                    import simplejson
                    retVal.insert(PROCESSED, simplejson.loads(retVal[RAW]))
                except ImportError:
                    raise PostRankException("missing library: simplejson is not installed")

            return retVal
        finally:
            c.close()

class PostRankException(Exception):
    pass
