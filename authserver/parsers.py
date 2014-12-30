import logging
from rest_framework.parsers import JSONParser, FormParser


logger = logging.getLogger(__name__)


class BetterJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        logger.info('Using JSON Parser')
        return super(BetterJSONParser, self).parse(stream, media_type, parser_context)


class BetterFormParser(FormParser):
    def parse(self, stream, media_type=None, parser_context=None):
        logger.info('Using Form Parser')
        data = super(BetterFormParser, self).parse(stream, media_type, parser_context)
        # Convert QueryDict to dict
        data = data.dict()
        return data
