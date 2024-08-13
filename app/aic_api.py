import requests


class AIC_API:
    def __init__(self):
        self.base_url = "https://api.artic.edu/api/v1"
        self.search_artworks_endpoint = "/artworks/search"
        self.session = (
            requests.Session()
        )  # Use a session to persist parameters across requests

    def search_artworks(self, query):
        """
        Search for artworks based on a query string.

        :param query: The search query string.
        :return: JSON data containing search results.
        :raises Exception: If the request fails or returns a non-200 status code.
        """
        url = self.base_url + self.search_artworks_endpoint
        params = {"q": query}
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def get_artwork(self, artwork_id):
        """
        Retrieve details of a specific artwork by its ID.

        :param artwork_id: The ID of the artwork to retrieve.
        :return: JSON data containing the artwork details.
        :raises Exception: If the request fails or returns a non-200 status code.
        """
        url = f"{self.base_url}artworks/{artwork_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def get_artist(self, artist_id):
        """
        Retrieve details of a specific artist by their ID.

        :param artist_id: The ID of the artist to retrieve.
        :return: JSON data containing the artist details.
        :raises Exception: If the request fails or returns a non-200 status code.
        """
        url = f"{self.base_url}artists/{artist_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Handle the HTTP response and raise an exception if the status code is not 200.

        :param response: The HTTP response object.
        :return: JSON data from the response.
        :raises Exception: If the response status code is not 200.
        """
        if response.status_code != 200:
            raise Exception(
                f"API request failed with status code {response.status_code}: {response.text}"
            )
        return response.json()


aic_api = AIC_API()
