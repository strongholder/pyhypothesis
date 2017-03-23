pyhypothesis - A python API client for hypothes.is
==================================================

The provided client is a very simple API client to hypothes.is that supports all api calls as of march 2017 except the
create new user call.

License
-------
The project is licensed under the MIT license - see LICENSE.txt

TODO
----
* Implement the "Create a new user" API call and related authentication
* keep up to date with _`https://h.readthedocs.io/en/latest/api/`
* generate sphinx docs
* The code is tested manually but unit tests are needed

Contributing
------------
See CONTRIBUTING.rst


Examples
--------
The client supports only api token authentication and a new client instance is initialized as follows::

    from pyhypothesis.api import HypoClient
    client = HypoClient("<api-token-here>")

After initializing the client requests can be made like so::

    result1 = client.fetch_annotation('U62d1A-2Edd82gOoVMICqA')
    result2 = client.update_annotation('U62d1A-2Edd82gOoVMICqA', text="test 123")
    result3 = client.delete_annotation('U62d1A-2Edd82gOoVMICqA')
    result4 = client.search_annotations(
        group="4PvgDpPS",
        user="demo-user@hypothes.is",
        tags=["corrections"],
        url='https://random-demo-website.com/arbitrary_page.html'
    )
    user_profile = client.get_user_profile()
