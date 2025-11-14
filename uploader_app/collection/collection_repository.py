from typing import Any

import requests

from uploader_app.config import APPLICATION

def get_collections(data_url: str, languages: list[str], parent_id: str | None = None) -> list[dict[str, Any]]:
        """
        Fetch the list of collections (categories) from the remote API for
        a list of languages.

        The remote API expects `application` and `language` as query parameters,
        e.g. `...?application=webuddhist&language=en`.

        Returns a list in the form:

        [
            {
                "language": "en",
                "collections": [ ... raw API items ... ],
            },
            {
                "language": "bo",
                "collections": [ ... raw API items ... ],
            },
        ]
        """
        all_collections: list[dict[str, Any]] = []
        categories_url = f"{data_url}/v2/categories/"
        for language in languages:
            params = {
                "application": APPLICATION,
                "language": language,
                "parent_id": parent_id,
            }
            response = requests.get(categories_url, params=params)
            response.raise_for_status()

            all_collections.append(
                {
                    "language": language,
                    "collections": response.json(),
                }
            )
        return all_collections