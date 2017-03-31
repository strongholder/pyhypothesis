"""
pyhypothesis is a simple API client for hypothes.is
"""

__author__      = "Daniel Popov"
__license__ = "MIT"
__version__ = "1.0.1"
__credits__ = ["Daniel Popov"]

import requests

class HypoClient(object):
    ApiUrl = "https://hypothes.is/api"

    def __init__(self, api_key):
        self.set_api_key(api_key)

    def set_api_key(self, api_key):
        self._api_key = api_key

    def get_headers(self):
        headers = {
            "Authorization": "Bearer %s" % self._api_key,
            "Accept": "application/json",
            'user-agent': 'pyhypothesis/%s' % __version__
        }

        return headers

    def make_request(self, url, method_name="get", payload=None, json_payload=None):
        call_kwargs = {}
        headers = self.get_headers()

        if payload is not None:
            call_kwargs["params"] = payload

        if json_payload is not None:
            call_kwargs["json"] = json_payload

        if headers:
            call_kwargs["headers"] = headers

        request_method = getattr(requests, method_name)

        r = request_method("%s%s" % (self.ApiUrl, url), **call_kwargs)
        response = r.json()

        return response

    def get_number_of_chunks(self, total, limit):
        if total <= limit:
            number_of_chunks = 1
        elif total % limit > 0:
            number_of_chunks = (total / limit) + 1
        else:
            number_of_chunks = total / limit

        return number_of_chunks

    def search_annotations(self, **kwargs):
        """

        client.search_annotations(
            group="4PvgDpPS",
            user="demo-user@hypothes.is",
            tags=["corrections"],
            url='https://random-demo-website.com/arbitrary_page.html'
        )

        :param kwargs: dict

        :return: dict
        """
        user = kwargs.get("user")
        tag = kwargs.get("tags")
        url = kwargs.get("url")
        group = kwargs.get("group")  # group code (not name, e.g. 4PvgDpPS)

        limit = kwargs.get("limit", 200)
        offset = kwargs.get("offset", 0)
        sort = kwargs.get("sort", "updated")
        order = kwargs.get("order", "desc")
        any = kwargs.get("any", None)
        fetch_all = kwargs.get("fetch_all", None)

        payload = {}

        if tag:
            payload["tag"] = tag

        if user:
            payload["user"] = user

        if url:
            payload["url"] = url

        if group:
            payload["group"] = group

        if any:
            payload["any"] = any

        if limit > 200:
            # the api only allows up to 200 records per request
            limit = 200

        payload["limit"] = limit
        payload["offset"] = offset
        payload["sort"] = sort
        payload["order"] = order

        if fetch_all:
            response = self.make_request("/search", payload=payload)
            total = response.get("total", 0)
            number_of_chunks = self.get_number_of_chunks(total, limit)
            chunks = [[(x * limit), x * limit + limit] for x in range(number_of_chunks)][1:]

            for chunk in chunks:
                payload["offset"] = chunk[0]
                payload["limit"] = limit

                resp = self.make_request("/search", payload=payload)
                response["rows"] += resp["rows"]

        else:
            response = self.make_request("/search", payload=payload)

        return response

    def fetch_annotation(self, annotation_id):
        """
        :param annotation_id: str e.g. (Ljtl4A8SEeeGq--uLluVdQ)

        :return: dict
        """

        response = self.make_request("/search", payload={
            "id": annotation_id
        })

        return response

    def create_annotation(self, group=None, permissions=None, references=(), tags=(), target=(), text="", uri=""):
        """
        Creates a new annotation

        :param group: group code (e.g. 4PvgDpPS)
        :param permissions: dict
        :param references: tuple of string
        :param tags: tuple of string
        :param target: tuple
        :param text: str
        :param uri: str

        :return: dict
        """

        payload = {}

        if group:
            payload["group"] = group

        if permissions:
            payload["permissions"] = permissions

        payload["references"] = references
        payload["tags"] = tags
        payload["target"] = target
        payload["text"] = text
        payload["uri"] = uri

        response = self.make_request("/annotations", method_name="post", json_payload=payload)

        return response


    def update_annotation(self, annotation_id, group=None, permissions=None, references=(), tags=(), target=(), text=None, uri=""):
        """
        Creates a new annotation

        :param annotation_id: str
        :param group: group code (e.g. 4PvgDpPS)
        :param permissions: dict
        :param references: tuple of string
        :param tags: tuple of string
        :param target: tuple
        :param text: str
        :param uri: str

        :return: dict
        """

        payload = {}

        if group:
            payload["group"] = group

        if permissions:
            payload["permissions"] = permissions

        if references:
            payload["references"] = references

        if tags:
            payload["tags"] = tags

        if target:
            payload["target"] = target

        if text is not None:
            payload["text"] = text

        if uri:
            payload["uri"] = uri

        response = self.make_request("/annotations/%s" % annotation_id, method_name="put", json_payload=payload)

        return response

    def delete_annotation(self, annotation_id):
        """
        Deletes an annotation

        :param annotation_id: str

        :return: dict
        """

        response = self.make_request("/annotations/%s" % annotation_id, method_name="delete", payload={})

        return response

    def get_user_profile(self, authority="hypothes.is"):
        """
        Returns the profile information for the authenticated user.

        :param authority: str
        :return:
        """

        response = self.make_request("/profile", payload={
            "authority": authority
        })

        return response


    def create_new_user(self, authority, username, email):
        """
        Creates a new user

        :param authority: str
        :param username: str
        :param email: str
        :return:
        """
        raise NotImplementedError
