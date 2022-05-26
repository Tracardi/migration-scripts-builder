from app.domain.exceptions import ElasticClientException
from app.service.config import config
from app.service.client import ElasticClient
from app.service.find_mappings_difference import find_mappings_difference
from pprint import pprint


def main():

    client = ElasticClient(config.elastic_host)
    new_codename = input("Provide a codename of your current Tracardi version:\n")

    try:
        new_indices = client.indices_for_codename(new_codename)

        old_codename = input("Provide a codename of your old Tracardi version:\n")
        old_indices = client.indices_for_codename(old_codename)

        differences = find_mappings_difference(old_indices, new_indices)
        pprint(differences, depth=5)

    except ElasticClientException as e:
        client.close()
        print(f"Error info: {str(e)}")
        return

    client.close()


if __name__ == "__main__":
    main()
