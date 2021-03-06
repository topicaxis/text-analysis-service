from os import path
from types import ModuleType
import logging


class Configuration(dict):
    def __init__(self, *args, **kwargs):
        super(Configuration, self).__init__(*args, **kwargs)

        # TODO: the default configuration should be moved to a separate module
        # and loaded from there instead
        self["CONSUL_HOST"] = None
        self["CONSUL_PORT"] = 8500
        self["CONSUL_SCHEME"] = "http"
        self["CONSUL_VERIFY_SSL"] = True
        self["CONSUL_HEALTH_INTERVAL"] = "10s"
        self["CONSUL_HEALTH_TIMEOUT"] = "5s"
        self["SERVICE_NAME"] = "tas"
        self["SENTRY_DSN"] = None
        self["SENTRY_LOG_LEVEL"] = logging.ERROR
        self["WORKER_MAX_REQUESTS"] = 100
        self["WORKER_MAX_REQUESTS_JITTER"] = 10
        self["WORKERS"] = 2
        self["HOST"] = "localhost"
        self["PORT"] = 8020
        self["LOG_LEVEL"] = logging.INFO
        self["LOG_FILE"] = None
        self["LOG_FILE_COUNT"] = 5
        self["LOG_FILE_MAX_SIZE"] = 1000000
        self["LOG_HANDLERS"] = []
        self["KEYWORD_STOP_LIST"] = "SmartStoplist.txt"
        self["DEBUG"] = False
        self["TESTING"] = False

    @classmethod
    def load_from_py(cls, filename):
        filename = filename if path.isabs(filename) else path.abspath(filename)

        settings_module = ModuleType("configuration")
        settings_module.__file__ = filename

        with open(filename) as f:
            exec(compile(f.read(), filename, 'exec'), settings_module.__dict__)

        configuration = cls()

        for key in dir(settings_module):
            if not key.startswith("_"):
                configuration[key] = getattr(settings_module, key)

        return configuration
