from __future__ import absolute_import
from collections import OrderedDict
import logging

from domaintools import API
from dxlbootstrap.app import Application
from dxlclient.service import ServiceRegistrationInfo
from dxldomaintoolsservice.requesthandlers import DomainToolsRequestCallback


# Configure local logger
logger = logging.getLogger(__name__)


class DomainToolsService(Application):
    """
    The "DomainTools DXL Python Service" application class.
    """

    #: The DXL service type for the DomainTools API
    SERVICE_TYPE = "/opendxl-domaintools/service/domaintools"

    #: The name of the "General" section within the application configuration
    #: file
    GENERAL_CONFIG_SECTION = "General"
    #: The property used to specify the DomainTools API Key in the application
    #: configuration file
    GENERAL_API_KEY_CONFIG_PROP = "apiKey"
    #: The property used to specify the DomainTools API User in the application
    #: configuration file
    GENERAL_API_USER_CONFIG_PROP = "apiUser"

    def __init__(self, config_dir):
        """
        Constructor parameters:

        :param config_dir: The location of the configuration files for the
            application
        """
        super(DomainToolsService, self).__init__(
            config_dir,
            "dxldomaintoolsservice.config")
        self._api = None
        self._api_key = None
        self._api_user = None

    @property
    def domaintools_api(self):
        """
        Returns the DomainTools API client

        :return: The DomainTools API client
        """
        return self._api

    @property
    def client(self):
        """
        The DXL client used by the application to communicate with the DXL
        fabric
        """
        return self._dxl_client

    @property
    def config(self):
        """
        The application configuration (as read from the
        "dxldomaintoolsservice.config" file)
        """
        return self._config

    def on_run(self):
        """
        Invoked when the application has started running.
        """
        logger.info("On 'run' callback.")

    def on_load_configuration(self, config):
        """
        Invoked after the application-specific configuration has been loaded

        This callback provides the opportunity for the application to parse
        additional configuration properties.

        :param config: The application configuration
        """
        logger.info("On 'load configuration' callback.")

        # API Key
        try:
            self._api_key = config.get(self.GENERAL_CONFIG_SECTION,
                                       self.GENERAL_API_KEY_CONFIG_PROP)
        except Exception:
            pass
        if not self._api_key:
            raise Exception(
                "DomainTools API Key not found in configuration file: {0}"
                .format(self._app_config_path))

        # API User
        try:
            self._api_user = config.get(self.GENERAL_CONFIG_SECTION,
                                        self.GENERAL_API_USER_CONFIG_PROP)
        except Exception:
            pass
        if not self._api_user:
            raise Exception(
                "DomainTools API User not found in configuration file: {0}"
                .format(self._app_config_path))

        self._api = API(self._api_user, self._api_key)

    def on_dxl_connect(self):
        """
        Invoked after the client associated with the application has connected
        to the DXL fabric.
        """
        logger.info("On 'DXL connect' callback.")

    def on_register_services(self):
        """
        Invoked when services should be registered with the application
        """
        # For methods where "query" is the only required parameter (the
        # majority)
        query_param = ["query"]

        # List of callbacks to register. Each item's key is the name of the
        # service to register. The associated value for each item is a list
        # of parameters which are required when invoking the service.
        callbacks = OrderedDict((
            ("account_information", None),
            ("brand_monitor", query_param),
            ("domain_profile", query_param),
            ("domain_search", query_param),
            ("domain_suggestions", query_param),
            ("host_domains", ["ip"]),
            ("hosting_history", query_param),
            ("ip_monitor", query_param),
            ("ip_registrant_monitor", query_param),
            ("iris", None),
            ("name_server_monitor", query_param),
            ("parsed_whois", query_param),
            ("phisheye", query_param),
            ("phisheye_term_list", None),
            ("registrant_monitor", query_param),
            ("reputation", query_param),
            ("reverse_ip", ["domain"]),
            ("reverse_ip_whois", None),
            ("reverse_name_server", query_param),
            ("reverse_whois", query_param),
            ("whois", query_param),
            ("whois_history", query_param)))

        # Register service 'domaintools_service'
        logger.info("Registering service: domaintools_service")
        service = ServiceRegistrationInfo(
            self._dxl_client,
            "/opendxl-domaintools/service/domaintools")

        for service_name, required_params in callbacks.items():
            logger.info(
                "Registering request callback: domaintools_%s_requesthandler",
                service_name)
            self.add_request_callback(service,
                                      "{}/{}".format(self.SERVICE_TYPE,
                                                     service_name),
                                      DomainToolsRequestCallback(
                                          self,
                                          service_name,
                                          required_params),
                                      False)

        self.register_service(service)
