# This sample invokes and displays the results of a DomainTools "Reverse IP
# Whois" via DXL.
#
# https://www.domaintools.com/resources/api-documentation/reverse-ip-whois/

import os
import sys

from dxlbootstrap.util import MessageUtils
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Message, Request

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:
    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    request_topic = "/opendxl-domaintools/service/domaintools/reverse_ip_whois"
    req = Request(request_topic)
    MessageUtils.dict_to_json_payload(req, {"query": "google"})
    res = client.sync_request(req, timeout=30)
    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        res_dict = MessageUtils.json_payload_to_dict(res)
        print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
    else:
        print("Error invoking service with topic '{}': {} ({})".format(
            request_topic, res.error_message, res.error_code))
