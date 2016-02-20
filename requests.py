"""
This is a module that implements class for nice requests building.

REQUESTS array has this structure:
    "REQUEST NAME": ["GET" or "POST",
                     "relative path to API link",
                     "type of header to be embedded into packet",
                     "Body of the requests"]
"""


class Request(object):
    """
    Class for building nice api requests
    """
    LONG_HEADER = {'X-Requested-With': 'XMLHttpRequest',
                   '__RequestVerificationToken': '',
                   'Connection': 'keep-alive',
                   'Cookie': ''}

    SHORT_HEADER = {'X-Requested-With': 'XMLHttpRequest',
                    'Cookie': ''}

    REQUESTS = {"API_GET_SESSION_TOKEN": ["GET", "/api/webserver/SesTokInfo",
                                          SHORT_HEADER, ""],
                "API_LOGIN_USER": ["POST", "/api/user/login",
                                   LONG_HEADER, "<?xml version=\"1.0\" "
                                                "encoding=\"UTF-8\"?>"
                                                "<request>"
                                                "<Username>admin</Username>"
                                                "<Password>{0}</Password>"
                                                "<password_type>4</password_type>"
                                                "</request>"],
                "API_LOGOUT_USER": ["POST", "/api/user/logout",
                                    LONG_HEADER, "<?xml version=\"1.0\" "
                                                 "encoding=\"UTF-8\"?>"
                                                 "<request>"
                                                 "<Logout>1</Logout>"
                                                 "</request>"],
                "API_DEVICE_INFO": ["GET", "/api/device/information",
                                    SHORT_HEADER, ""],
                "API_SIGNAL_PARAMETERS": ["GET", "/api/device/signal",
                                          SHORT_HEADER, ""]
                }

    def __init__(self, rtype='', path='', header='', body=''):
        self._rtype = rtype
        self._path = path
        self._header = header
        self._body = body

    @classmethod
    def prepared_request(cls, request):
        rtype, path, header, body = cls.REQUESTS[request]
        return cls(rtype, path, header, body)

    @property
    def rtype(self):
        """
        returns current request type
        :return: 'GET' or 'POST'
        """
        return self._rtype

    @rtype.setter
    def rtype(self, rtype):
        """
        sets current request type
        :param rtype: 'GET' or 'POST'
        """
        self._rtype = rtype

    @property
    def path(self):
        """
        returns current request path to api call
        :return: '/api/.../...'
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        sets current request path to api call
        :param path: '/api/.../...'
        """
        self._path = path

    @property
    def header(self):
        """
        returns current request header
        :return: SHORT or LONG header
        """
        return self._header

    @header.setter
    def header(self, header):
        """
        sets current request header
        :param header: SHORT or LONG header
        """
        self._header = header

    @property
    def body(self):
        """
        returns current request body
        :return: current body of the request
        """
        return self._body

    @body.setter
    def body(self, body):
        """
        sets current request body
        :param body: current body of the request
        """
        self._body = body
