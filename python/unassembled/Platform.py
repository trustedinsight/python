
class Pubnub(PubnubCore):
    def __init__(
        self,
        publish_key,
        subscribe_key,
        secret_key = False,
        cipher_key = False,
        ssl_on = False,
        origin = 'pubsub.pubnub.com',
        pres_uuid = None,
        auth_key = None
    ) :
        super(Pubnub, self).__init__(
            publish_key = publish_key,
            subscribe_key = subscribe_key,
            secret_key = secret_key,
            cipher_key = cipher_key,
            ssl_on = ssl_on,
            origin = origin,
            uuid = pres_uuid,
            auth_key = auth_key
        )        

    def _request( self, request, callback = None ) :
        ## Build URL
        url = self.getUrl(request)
        usock = None
        response = None

        ## Send Request Expecting JSONP Response
        try:
            try: usock = urllib2.urlopen( url, None, 310 )
            except urllib2.HTTPError, e: response = e.fp.read()
            except TypeError: usock = urllib2.urlopen( url, None )
            if (response == None): response = usock.read()
            if (usock != None): usock.close()
            resp_json = json.loads(response)
        except Exception as e:
            return None
            
        if (callback):
            callback(resp_json)
        else:
            return resp_json
