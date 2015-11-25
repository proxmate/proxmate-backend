import threading
from elasticsearch import Elasticsearch
from datetime import timedelta, datetime
from django.conf import settings

elastic_credentials = ""

# check if it needs authentication
if settings.ELASTICSEARCH_USERNAME and settings.ELASTICSEARCH_PASSWORD:
    elastic_credentials = settings.ELASTICSEARCH_USERNAME + ":" + settings.ELASTICSEARCH_PASSWORD + "@"

elastic = Elasticsearch(elastic_credentials + settings.ELASTICSEARCH_ADDRESS + ':' + str(settings.ELASTICSEARCH_PORT) + '/')

class ElasticThreadEnabled(threading.Thread):
    """
    Log data in elasticsearch for reporting
    """
    def __init__(self, doc_type, user, req, index=settings.ELASTICSEARCH_INDEX):
        """
        Log data in elasticsearch for reporting
        :param doc_type: document type for es.
        :param user: user that made the request.
        :param req: request object.
        """
        _user = {
            "timestamp": datetime.now()
        }

        if user:
            _user["is_updated"] = user.profile.is_updated_user if user.profile.is_updated_user else 'None'
            _user["id"] = user.id
            _user["username"] = user.username

        if req:
            _user["os_name"] = req.user_agent.os.family if req.user_agent.os.family else 'None',
            _user["browser_name"] = req.user_agent.browser.family if req.user_agent.browser.family else 'None',
            _user["country"] = req.location['country_name'] if req.location['country_name'] else 'None',

        self.doc_type = doc_type
        self.body = _user
        self.index = index
        threading.Thread.__init__(self)

    def run(self):
        """
        Send data to elasticsearc
        """
        elastic.index(index=self.index, doc_type=self.doc_type, body=self.body)


class ElasticThreadDisabled(threading.Thread):
    """
    In case sending is disabled from configuration
    """
    def __init__(self, index, doc_type, body):
        threading.Thread.__init__(self)

    def run(self):
        pass

# check settings and apply them
if settings.ELASTICSEARCH_ENABLED:
    ElasticThread = ElasticThreadEnabled
else:
    ElasticThread = ElasticThreadDisabled