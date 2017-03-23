"""
pyhypothesis is a simple API client for hypothes.is
"""

__author__      = "Daniel Popov"
__license__ = "MIT"
__version__ = "1.0.0"
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
            'user-agent': 'pyhypothesis/1.0.0'
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

        import pprint
        pprint.pprint(call_kwargs)

        r = request_method("%s%s" % (self.ApiUrl, url), **call_kwargs)
        response = r.json()

        return response

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

        limit = kwargs.get("limit", 20)
        offset = kwargs.get("offset", 0)
        sort = kwargs.get("sort", "updated")
        order = kwargs.get("order", "desc")
        any = kwargs.get("any", None)


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

        payload["limit"] = limit
        payload["offset"] = offset
        payload["sort"] = sort
        payload["order"] = order

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
