from app.domain.exceptions import ElasticClientException
from app.service.config import config
from app.service.client import ElasticClient
from app.domain.index_difference import IndexDifference
from app.service.difference_finder import DifferenceFinder
from app.service.save_manager import SaveManager


def main():

    client = ElasticClient(config.elastic_host)
    new_codename = input("Provide a codename of your current Tracardi version:\n")
    old_codename = input("Provide a codename of your old Tracardi version:\n")

    try:
        old_indices = client.mappings_for_codename(old_codename)
        new_indices = client.mappings_for_codename(new_codename)
        client.close()

        common_indices = set(new_indices.keys()).intersection(old_indices.keys())

        removed_indices = set(old_indices.keys()) - set(new_indices.keys())
        added_indices = set(new_indices.keys()) - set(old_indices.keys())
        comment = f"Added indices: {', '.join(added_indices)}; removed indices: {', '.join(removed_indices)}"

        diffs = [
            IndexDifference(
                name=key,
                difference=DifferenceFinder(
                    old_mapping=old_indices[key].mapping,
                    new_mapping=new_indices[key].mapping
                ).get_difference(),
                multi=old_indices[key].multi and new_indices[key].multi,
            )
            for key in common_indices
        ]

        migrations = [diff.to_migration().build_migration() for diff in diffs]

        mig_name = input("How would you like to name your migration?\n")

        SaveManager.save_migrations([comment, *migrations], mig_name)

    except ElasticClientException as e:
        client.close()
        print(f"Error info: {str(e)}")
        return


if __name__ == "__main__":
    main()
