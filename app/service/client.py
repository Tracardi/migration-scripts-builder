from elasticsearch import Elasticsearch, AuthenticationException
from pydantic import AnyHttpUrl
from app.domain.exceptions import ElasticClientException


class ElasticClient:

    def __init__(self, host: AnyHttpUrl):
        self._client = Elasticsearch(hosts=host)

    def indices_for_codename(self, codename: str):
        try:
            indices_names = self._client.indices.get(index=f"{codename}-tracardi-*" if codename else "tracardi-*")

            result = {}
            for index_name in indices_names:
                result.update(**self._client.indices.get_mapping(index=index_name).body)

            if codename:
                result = {key.split(codename)[1][1:]: result[key] for key in result}

            return result

        except AuthenticationException as e:
            print("Invalid Elasticsearch authentication credentials provided.")
            raise ElasticClientException(str(e))

    def close(self):
        self._client.close()
