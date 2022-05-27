from elasticsearch import Elasticsearch, AuthenticationException
from pydantic import AnyHttpUrl
from app.domain.exceptions import ElasticClientException
from app.service.find_field_types import find_field_types
import re


class ElasticClient:

    def __init__(self, host: AnyHttpUrl):
        self._client = Elasticsearch(hosts=host)

    def mappings_for_codename(self, codename: str):
        try:
            indices_names = self._client.indices.get(index=f"{codename}-tracardi-*" if codename else "tracardi-*")

            result = {}
            for index_name in indices_names:
                result.update(**self._client.indices.get_mapping(index=index_name).body)

            if codename:
                result = {key.split(codename)[1][1:]: result[key] for key in result}

            result = {
                re.split(r"-[0-9]{4}-[0-9]{1,2}", key)[0]: {
                    "mapping": find_field_types(result[key]["mappings"]["properties"]),
                    "multi": bool(re.findall(r"-[0-9]{4}-[0-9]{1,2}", key))
                } for key in result
            }

            return result

        except AuthenticationException as e:
            print("Invalid Elasticsearch authentication credentials provided.")
            raise ElasticClientException(str(e))

    def close(self):
        self._client.close()
