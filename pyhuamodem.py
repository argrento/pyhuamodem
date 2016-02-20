"""
Modem base class
"""

import logging
from xml.dom.minidom import *
import hashlib
import base64
import collections
from urllib3 import HTTPConnectionPool

from errors import *
from requests import *


class Modem(object):
    """
    Modem base class
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, ip_address='192.168.8.1',
                 username='admin',
                 password='admin'):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.pool = None
        self.session = None
        self.token = None
        self.cookie = None
        self.is_connected = False
        self.modem_info = {'DeviceName': None,
                           'SerialNumber': None,
                           'Imei': None,
                           'Imsi': None,
                           'Iccid': None,
                           'Msisdn': None,
                           'HardwareVersion': None,
                           'SoftwareVersion': None,
                           'WebUIVersion': None,
                           'MacAddress1': None,
                           'MacAddress2': None,
                           'ProductFamily': None,
                           'Classify': None,
                           'supportmode': None,
                           'workmode': None}
        self.signal_parameters = {'pci': None,
                                  'sc': None,
                                  'cell_id': None,
                                  'rsrq': None,
                                  'rsrp': None,
                                  'rssi': None,
                                  'sinr': None,
                                  'rscp': None,
                                  'ecio': None,
                                  'mode': None}
        self.dhcp_settings = {'DhcpIPAddress': None,
                              'DhcpLanNetmask': None,
                              'DhcpStatus': None,
                              'DhcpStartIPAddress': None,
                              'DhcpEndIPAddress': None,
                              'DhcpLeaseTime': None,
                              'DnsStatus': None,
                              'PrimaryDns': None,
                              'SecondaryDns': None}

    def connect(self):
        """
        connects to the modem via opening HTTPConnectionPool
        :return:
        """
        self.pool = HTTPConnectionPool(self.ip_address, maxsize=1)
        self.is_connected = True

    def disconnect(self):
        """
        disconnects from the modem via closing HTTPConnectionPool
        :return:
        """
        self.pool.close()

    def session_token(self):
        """
        returns session Id and token Id.
        :return:
        """
        return self.session, self.token

    def send_request(self, request):
        """
        sends an api request to the modem
        :param request: is a request to be sent
        :return: request answer
        """

        try:
            response = self.pool.request(request.rtype, request.path,
                                         headers=request.header,
                                         body=request.body)
        except AttributeError:
            raise UserWarning("Should call 'connect()' at first")

        parsed_answer = parseString(response.data)

        # trying to detect an error
        error = parsed_answer.getElementsByTagName('error')
        if error:
            error_code = \
                parsed_answer.getElementsByTagName('code')[0].childNodes[
                    0].nodeValue
            if error_code == '100002':
                raise ErrorSystemNotSupport("System do not support "
                                            "this feature.")
            elif error_code == '100003':
                raise ErrorSystemNoRights("You have no rights to"
                                          "perform this action.")
            elif error_code == '100004':
                raise ErrorSystemBusy("System is busy.")
            elif error_code == '108001':
                raise ErrorLoginUsernameWrong("Wrong username.")
            elif error_code == '108002':
                raise ErrorLoginPasswordWrong("Wrong password.")
            elif error_code == '108003':
                raise ErrorUserAlreadyLogin("User is already logged in.")
            elif error_code == '108006':
                raise ErrorLoginUsernamePwdWrong("Wrong username and password.")
            elif error_code == '120001':
                raise ErrorVoiceBusy("Modem is busy with the voice call.")
            elif error_code == '125001':
                raise ErrorWrongToken("Trying to make an api "
                                      "call with the wrong token.")
            elif error_code == '125002':
                raise ErrorWrongSession("Trying to make an api "
                                        "call with the wrong session.")
            elif error_code == '125003':
                raise ErrorWrongSessionToken("Trying to make an api call "
                                             "with the wrong session token.")
            else:
                raise ErrorUnknownError("Unknown error.")

        # request is fine, return it
        return response

    def start_new_session(self):
        """
        Function performs a call to the /api/webserver/SesTokInfo, which
        generates a new pair of session info and token info. This overrides
        an old pair.
        :return:
        """
        _request = Request.prepared_request('API_GET_SESSION_TOKEN')
        response = self.send_request(_request)
        _xml = parseString(response.data)
        self.session = _xml.getElementsByTagName('SesInfo')[0].childNodes[
            0].nodeValue
        self.token = _xml.getElementsByTagName('TokInfo')[0].childNodes[
            0].nodeValue

    def login(self):
        """
        Function performs a call to the /api/user/login
        This a mandatory call to enable almost 90% of api features.
        If login is successful, the new session is returned in the answer.
        :return: a response after login
        """
        # a request for login
        _request = Request.prepared_request('API_LOGIN_USER')

        # add session and token info to the header
        _request.header['Cookie'] = self.session
        _request.header['__RequestVerificationToken'] = self.token

        # computing the password hash
        pass_hash = base64.b64encode(hashlib.sha256(self.password).hexdigest())
        login_hash = base64.b64encode(hashlib.sha256(
                self.username + pass_hash + self.token).hexdigest());

        # add password hash to the request body
        _request.body = _request.body.format(login_hash)

        # send request to the modem
        response = self.send_request(_request)

        # save new session and token info
        self.session = response.headers['Set-Cookie'].split(';')[0]
        self.token = response.headers['__RequestVerificationTokenone'].split(';')[0]
        return response

    def logout(self):
        """
        Logout current (only one) user
        :return:
        """
        # request to logout
        _request = Request.prepared_request('API_LOGOUT_USER')

        # set up request security parameters
        _request.header['Cookie'] = self.session
        _request.header['__RequestVerificationToken'] = self.token

        # send request
        response = self.send_request(_request)
        return response

    def call_modem_info(self):
        """
        Calls modem information parameters from the modem
        :return: dict with info
        """
        _request = Request.prepared_request('API_DEVICE_INFO')
        _request.header['Cookie'] = self.session
        response = self.send_request(_request)

        _xml = parseString(response.data)

        # fill the device information structure
        for parameter in self.modem_info:
            try:
                self.modem_info[parameter] = _xml.getElementsByTagName(
                        parameter)[0].childNodes[0].nodeValue
            except IndexError:
                self.modem_info[parameter] = None
        return self.modem_info

    def get_modem_info(self):
        """
        returns modem information without calling it from the modem
        :return: dict with info
        """
        return self.modem_info

    def call_signal_parameters(self):
        """
        Calls signal parameters
        :return: dict with parameters
        """
        _request = Request.prepared_request('API_SIGNAL_PARAMETERS')
        _request.header['Cookie'] = self.session
        response = self.send_request(_request)

        _xml = parseString(response.data)

        # fill the device information structure
        for parameter in self.signal_parameters:
            try:
                self.signal_parameters[parameter] = _xml.getElementsByTagName(
                        parameter)[0].childNodes[0].nodeValue
            except IndexError:
                self.signal_parameters[parameter] = None
        return self.signal_parameters

    def get_signal_parameters(self):
        """
        returns signal parameters without calling them from the server
        :return:
        """
        return self.signal_parameters

if __name__ == "__main__":
    modem = Modem(ip_address='192.168.8.1', password='admin1')
    modem.connect()
    modem.start_new_session()
    modem.login()
    print(modem.call_signal_parameters())
    modem.logout()
    modem.disconnect()
