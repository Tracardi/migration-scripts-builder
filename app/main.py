from app.domain.exceptions import ElasticClientException
from app.service.config import config
from app.service.client import ElasticClient
from pprint import pprint
from app.service.compare_mappings import compare_mappings
from app.service.build_script import build_script


def main():

    client = ElasticClient(config.elastic_host)
    new_codename = input("Provide a codename of your current Tracardi version:\n")
    old_codename = input("Provide a codename of your old Tracardi version:\n")

    try:
        old_indices = client.mappings_for_codename(old_codename, new_codename == old_codename)
        new_indices = client.mappings_for_codename(new_codename)
        client.close()

        indices = {
            key: {
                "differences": compare_mappings(old_indices[key]["mapping"], new_indices[key]["mapping"]),
                "multi": old_indices[key]["multi"] and new_indices[key]["multi"]
            }
            for key in set(new_indices.keys()).intersection(old_indices.keys())
        }

        pprint(indices["tracardi-event"]['differences'])

        scripts = {key: build_script(indices[key]["differences"]) for key in indices}

    except ElasticClientException as e:
        client.close()
        print(f"Error info: {str(e)}")
        return


if __name__ == "__main__":
    main()
