import logging

from elasticsearch import Elasticsearch, AuthenticationException
from pydantic import AnyHttpUrl
from app.domain.exceptions import ElasticClientException
import re
from app.domain.index import Index
from typing import Dict


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class ElasticClient:

    def __init__(self, host: AnyHttpUrl):
        self._client = Elasticsearch(hosts=host)

    def mappings_for_codename(self, codename: str) -> Dict[str, Index]:
        """
        :param codename: codename of the version
        Returns all found indices for the version with given codename.
        """
        index_name_template = f"{codename}.tracardi-*" if codename else "tracardi-*"

        try:
            indices_names = self._client.indices.get(index=index_name_template)

            print(indices_names)

            result = {}
            for index_name in indices_names:
                result.update(**self._client.indices.get_mapping(index=index_name))

            if codename:
                result = {key.split(codename)[1][1:]: result[key] for key in result}

            result = {
                re.split(r"-[0-9]{4}-[0-9]{1,2}", key)[0]: Index(
                    name=re.split(r"-[0-9]{4}-[0-9]{1,2}", key)[0],
                    multi=bool(re.findall(r"-[0-9]{4}-[0-9]{1,2}", key)),
                    mapping=Index.standardize_mapping(result[key]["mappings"]["properties"])
                ) for key in result
            }

            return result

        except AuthenticationException as e:
            print("Invalid Elasticsearch authentication credentials provided.")
            raise ElasticClientException(str(e))

    def close(self):
        self._client.close()
