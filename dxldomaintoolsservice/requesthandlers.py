import logging

from domaintools.exceptions import ServiceException
from dxlclient.callbacks import RequestCallback
from dxlclient.message import Response, ErrorResponse
from dxlbootstrap.util import MessageUtils


# Configure local logger
logger = logging.getLogger(__name__)


class DomainToolsRequestCallback(RequestCallback):
    """
    Request callback used to invoke the DomainTools REST API
    """
    def __init__(self, app, func_name, required_params=None):
        """
        Constructor parameters:

        :param app: The application this handler is associated with
        """
        super(DomainToolsRequestCallback, self).__init__()
        self._app = app
        self._func_name = func_name
        self._required_params = required_params

    def on_request(self, request):
        """
        Invoked when a request message is received.

        :param request: The request message
        """
        # Handle request
        logger.info("Request received on topic: '{0}' with payload: '{1}'".format(
            request.destination_topic, MessageUtils.decode_payload(request)))

        try:
            res = Response(request)

            try:
                request_dict = MessageUtils.json_payload_to_dict(request)
            except Exception:
                request_dict = {}

            # Ensure required parameters are present
            if self._required_params:
                for name in self._required_params:
                    if name not in request_dict:
                        raise Exception("Required parameter not found: '{0}'".format(name))

            if "format" not in request_dict:
                request_dict["format"] = "json"

            # Invoke DomainTools API via client
            dt_response = getattr(self._app.domaintools_api, self._func_name)(**request_dict)

            # Set response payload
            response_data = dt_response.data()
            if type(response_data) is dict:
                MessageUtils.dict_to_json_payload(res, response_data)
            else:
                MessageUtils.encode_payload(res, response_data)
        except ServiceException as ex:
            logger.exception("Error handling request")
            msg = "%s: %s" % (ex.__class__.__name__, ex.reason)
            res = ErrorResponse(request, MessageUtils.encode(msg))

        except Exception as ex:
            logger.exception("Error handling request")
            msg = str(ex)
            if len(msg) == 0:
                msg = ex.__class__.__name__
            res = ErrorResponse(request, MessageUtils.encode(msg))

        # Send response
        self._app.client.send_response(res)
