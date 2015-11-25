import urllib, md5, datetime, dateutil.parser, pytz
from cgi import parse_qs
from time import time
from django.conf import settings
from urllib import urlencode
from urllib2 import urlopen, Request

TZINFOS = {
    'PDT': pytz.timezone('US/Pacific'),
}

def paypal_date_to_utc(paypal_date):
    datetime_in_pdt = dateutil.parser.parse(paypal_date, tzinfos=TZINFOS)
    print paypal_date, datetime_in_pdt, datetime_in_pdt.astimezone(pytz.utc)
    return datetime_in_pdt.astimezone(pytz.utc)

def verify_ipn(data):
    # prepares provided data set to inform PayPal we wish to validate the response
    data["cmd"] = "_notify-validate"
    params = urlencode(data)

    # sends the data and request to the PayPal Sandbox
    req = Request(settings.PAYPAL_ACTION_URL, params)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    # reads the response back from PayPal
    response = urlopen(req)
    status = response.read()

    # If not verified
    if not status == "VERIFIED":
        return False

    # if not the correct currency
    if not data["mc_currency"] == "USD":
        return False

    # otherwise...
    return True


class PayPal:
    """ #PayPal utility class"""
    signature_values = {}
    API_ENDPOINT = ""
    PAYPAL_URL = ""

    def __init__(self):
        ## Sandbox values
        self.signature_values = {
            'USER': 'support-facilitator_api1.proxmate.me',  # Edit this to your API user name
            'PWD': 'B8JL5YMF92WGS4HW',  # Edit this to your API password
            'SIGNATURE': 'AFcWxV21C7fd0v3bYYYRCpSSRl31Ag6IOulOr..-abl1MrjT-BobyL8l',  # edit this to your API signature
            'VERSION': '124.0',
        }
        self.API_ENDPOINT = 'https://api-3t.sandbox.paypal.com/nvp'  # Sandbox URL, not production
        self.PAYPAL_URL = 'https://www.sandbox.paypal.com/webscr&cmd=_express-checkout&token='
        self.signature = urllib.urlencode(self.signature_values) + "&"

    # API METHODS
    def SetExpressCheckout(self, amount, return_url, cancel_url, email, **kwargs):
        params = {
            'METHOD': "SetExpressCheckout",
            'NOSHIPPING': 1,
            'L_BILLINGTYPE0': 'RecurringPayments',
            'L_BILLINGAGREEMENTDESCRIPTION0': 'alabala',
            'PAYMENTACTION': 'Authorization',
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'CUSTOM': email,
            'AMT': amount,
        }
        params.update(kwargs)
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_dict = parse_qs(response)
        response_token = response_dict['TOKEN'][0]
        return response_token

    def GetExpressCheckoutDetails(self, token, return_all=False):
        params = {
            'METHOD': "GetExpressCheckoutDetails",
            'RETURNURL': 'http://www.yoursite.com/returnurl',  # edit this
            'CANCELURL': 'http://www.yoursite.com/cancelurl',  # edit this
            'TOKEN': token,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_dict = parse_qs(response)
        if return_all:
            return response_dict
        try:
            response_token = response_dict['TOKEN'][0]
        except KeyError:
            response_token = response_dict
        return response_token

    def DoExpressCheckoutPayment(self, token, payer_id, amt):
        params = {
            'METHOD': "DoExpressCheckoutPayment",
            'PAYMENTACTION': 'Sale',
            'RETURNURL': 'http://www.yoursite.com/returnurl',  # edit this
            'CANCELURL': 'http://www.yoursite.com/cancelurl',  # edit this
            'TOKEN': token,
            'AMT': amt,
            'PAYERID': payer_id,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])
        return response_tokens

    def GetTransactionDetails(self, tx_id):
        params = {
            'METHOD': "GetTransactionDetails",
            'TRANSACTIONID': tx_id,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])
        return response_tokens

    def MassPay(self, email, amt, note, email_subject):
        unique_id = str(md5.new(str(datetime.datetime.now())).hexdigest())
        params = {
            'METHOD': "MassPay",
            'RECEIVERTYPE': "EmailAddress",
            'L_AMT0': amt,
            'CURRENCYCODE': 'USD',
            'L_EMAIL0': email,
            'L_UNIQUE0': unique_id,
            'L_NOTE0': note,
            'EMAILSUBJECT': email_subject,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])
        response_tokens['unique_id'] = unique_id
        return response_tokens

    def DoDirectPayment(self, amt, ipaddress, acct, expdate, cvv2, firstname, lastname, cctype, street, city, state,
                        zipcode):
        params = {
            'METHOD': "DoDirectPayment",
            'PAYMENTACTION': 'Sale',
            'AMT': amt,
            'IPADDRESS': ipaddress,
            'ACCT': acct,
            'EXPDATE': expdate,
            'CVV2': cvv2,
            'FIRSTNAME': firstname,
            'LASTNAME': lastname,
            'CREDITCARDTYPE': cctype,
            'STREET': street,
            'CITY': city,
            'STATE': state,
            'ZIP': zipcode,
            'COUNTRY': 'United States',
            'COUNTRYCODE': 'US',
            'RETURNURL': 'http://www.yoursite.com/returnurl',  # edit this
            'CANCELURL': 'http://www.yoursite.com/cancelurl',  # edit this
            'L_DESC0': "Desc: ",
            'L_NAME0': "Name: ",
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])
        return response_tokens

    def CreateRecurringPaymentsProfile(self, token, startdate, desc, period, freq, amt):
        params = {
            'METHOD': 'CreateRecurringPaymentsProfile',
            'PROFILESTARTDATE': startdate,
            'DESC': desc,
            'BILLINGPERIOD': period,
            'BILLINGFREQUENCY': freq,
            'AMT': amt,
            'TOKEN': token,
            'CURRENCYCODE': 'USD',
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_dict = parse_qs(response)
        return response_dict

    def GetRecurringPaymentsProfileDetails(self, profile_id):
        params = {
            'METHOD': 'GetRecurringPaymentsProfileDetails',
            'PROFILEID': profile_id,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_dict = parse_qs(response)
        return response_dict

    def ManageRecurringPaymentsProfileStatus(self, profile_id, action):
        params = {
            'METHOD': 'ManageRecurringPaymentsProfileStatus',
            'PROFILEID': profile_id,
            'ACTION': action,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_dict = parse_qs(response)
        return response_dict
