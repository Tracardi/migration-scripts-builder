from app.domain.exceptions import ElasticClientException
from app.service.config import config
from app.service.client import ElasticClient
from pprint import pprint


def main():

    client = ElasticClient(config.elastic_host)
    new_codename = input("Provide a codename of your current Tracardi version:\n")
    old_codename = input("Provide a codename of your old Tracardi version:\n")

    try:
        old_indices = client.mappings_for_codename(old_codename)
        new_indices = client.mappings_for_codename(new_codename)
        client.close()

        pprint(old_indices["tracardi-event"])

    except ElasticClientException as e:
        client.close()
        print(f"Error info: {str(e)}")
        return


if __name__ == "__main__":
    main()
