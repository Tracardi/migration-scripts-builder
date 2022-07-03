from app.domain.exceptions import ElasticClientException
from app.service.config import config
from app.service.client import ElasticClient
from app.domain.index_difference import IndexDifference
from app.service.difference_finder import DifferenceFinder
from app.service.save_manager import SaveManager
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def main():
    client = ElasticClient(config.elastic_host)
    logger.info(msg="Provide a codename of your current Tracardi version:\n")
    new_codename = input()
    logger.info(msg="Provide a codename of your old Tracardi version:\n")
    old_codename = input()

    try:
        old_indices = client.mappings_for_codename(old_codename)
        new_indices = client.mappings_for_codename(new_codename)
        client.close()

        common_indices = set(new_indices.keys()).intersection(old_indices.keys())
        removed_indices = set(old_indices.keys()) - set(new_indices.keys())
        logger.info(msg=f"Found removed indices: {', '.join(removed_indices)}" if removed_indices else
                   "No removed indices found")

        added_indices = set(new_indices.keys()) - set(old_indices.keys())
        logger.info(msg=f"Found new indices: {', '.join(added_indices)}" if added_indices else
                   "No new indices found")
        comment = f"Added indices: {', '.join(added_indices)}; removed indices: {', '.join(removed_indices)}"

        diffs = []
        for key in common_indices:
            logger.info(msg=f"Processing common index '{key}'")
            diffs.append(
                IndexDifference(
                    from_index=key,
                    to_index=key,
                    difference=DifferenceFinder(
                        old_mapping=old_indices[key].mapping,
                        new_mapping=new_indices[key].mapping
                    ).get_difference(),
                    multi=old_indices[key].multi and new_indices[key].multi
                )
            )

        migrations = [diff.to_migration().build_migration() for diff in diffs]

        logger.info(msg="How would you like to name your migration?\n")
        mig_name = input()

        # TODO HANDLE RENAME

        SaveManager.save_migrations([comment, *migrations], mig_name)

    except ElasticClientException as e:
        client.close()
        logger.error(msg=f"Error info: {str(e)}")
        return


if __name__ == "__main__":
    main()
