import logging

from dxlbootstrap.app import Application
from dxlclient.service import ServiceRegistrationInfo
from requesthandlers import DomainToolsRequestCallback
from domaintools import API


# Configure local logger
logger = logging.getLogger(__name__)


class DomainToolsService(Application):
    """
    The "DomainTools DXL Python Service" application class.
    """

    #: The DXL service type for the DomainTools API
    SERVICE_TYPE = "/opendxl-domaintools/service/domaintools"

    #: The name of the "General" section within the application configuration file
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
        super(DomainToolsService, self).__init__(config_dir, "dxldomaintoolsservice.config")
        self._api = None

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
        The application configuration (as read from the "dxldomaintoolsservice.config" file)
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
            api_key = config.get(self.GENERAL_CONFIG_SECTION, self.GENERAL_API_KEY_CONFIG_PROP)
        except Exception:
            pass
        if not api_key:
            raise Exception("DomainTools API Key not found in configuration file: {0}"
                            .format(self._app_config_path))

        # API User
        try:
            api_user = config.get(self.GENERAL_CONFIG_SECTION, self.GENERAL_API_USER_CONFIG_PROP)
        except Exception:
            pass
        if not api_user:
            raise Exception("DomainTools API User not found in configuration file: {0}"
                            .format(self._app_config_path))

        self._api = API(api_user, api_key)

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
        # For methods where "query" is the only required parameter (the majority)
        QUERY_PARAM = ["query"]

        # Register service 'domaintools_service'
        logger.info("Registering service: {0}".format("domaintools_service"))
        service = ServiceRegistrationInfo(self._dxl_client, "/opendxl-domaintools/service/domaintools")
        logger.info("Registering request callback: {0}".format("domaintools_account_information_requesthandler"))
        self.add_request_callback(service, "{0}/account_information".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "account_information"), False)
        logger.info("Registering request callback: {0}".format("domaintools_brand_monitor_requesthandler"))
        self.add_request_callback(service, "{0}/brand_monitor".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "brand_monitor", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_domain_profile_requesthandler"))
        self.add_request_callback(service, "{0}/domain_profile".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "domain_profile", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_domain_search_requesthandler"))
        self.add_request_callback(service, "{0}/domain_search".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "domain_search", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_domain_suggestions_requesthandler"))
        self.add_request_callback(service, "{0}/domain_suggestions".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "domain_suggestions", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_hosting_history_requesthandler"))
        self.add_request_callback(service, "{0}/hosting_history".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "hosting_history", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_ip_monitor_requesthandler"))
        self.add_request_callback(service, "{0}/ip_monitor".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "ip_monitor", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_ip_registrant_monitor_requesthandler"))
        self.add_request_callback(service, "{0}/ip_registrant_monitor".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "ip_registrant_monitor", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_name_server_monitor_requesthandler"))
        self.add_request_callback(service, "{0}/name_server_monitor".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "name_server_monitor", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_parsed_whois_requesthandler"))
        self.add_request_callback(service, "{0}/parsed_whois".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "parsed_whois", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_registrant_monitor_requesthandler"))
        self.add_request_callback(service, "{0}/registrant_monitor".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "registrant_monitor", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_reputation_requesthandler"))
        self.add_request_callback(service, "{0}/reputation".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "reputation", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_reverse_ip_requesthandler"))
        self.add_request_callback(service, "{0}/reverse_ip".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "reverse_ip", ["domain"]), False)
        logger.info("Registering request callback: {0}".format("domaintools_host_domains_requesthandler"))
        self.add_request_callback(service, "{0}/host_domains".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "host_domains", ["ip"]), False)
        logger.info("Registering request callback: {0}".format("domaintools_reverse_ip_whois_requesthandler"))
        self.add_request_callback(service, "{0}/reverse_ip_whois".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "reverse_ip_whois"), False)
        logger.info("Registering request callback: {0}".format("domaintools_reverse_name_server_requesthandler"))
        self.add_request_callback(service, "{0}/reverse_name_server".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "reverse_name_server", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_reverse_whois_requesthandler"))
        self.add_request_callback(service, "{0}/reverse_whois".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "reverse_whois", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_whois_requesthandler"))
        self.add_request_callback(service, "{0}/whois".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "whois", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_whois_history_requesthandler"))
        self.add_request_callback(service, "{0}/whois_history".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "whois_history", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_phisheye_requesthandler"))
        self.add_request_callback(service, "{0}/phisheye".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "phisheye", QUERY_PARAM), False)
        logger.info("Registering request callback: {0}".format("domaintools_phisheye_term_list_requesthandler"))
        self.add_request_callback(service, "{0}/phisheye_term_list".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "phisheye_term_list"), False)
        logger.info("Registering request callback: {0}".format("domaintools_iris_requesthandler"))
        self.add_request_callback(service, "{0}/iris".format(self.SERVICE_TYPE),
                                  DomainToolsRequestCallback(self, "iris"), False)
        self.register_service(service)
