from typing import Optional
import requests


class API:


    def __init__(self, base_url):
        # remove "/" at the end if it exists
        base_url = base_url[:-1] if "/" == base_url[-1] else base_url
        self.base_url = base_url
        self.url = self.base_url
    


    def add_query(self, **kwargs):
        """
        Add query paramter to the API Endpoint

        Args:
            **kwargs : key-value pair(s) of the query (e.g.: subreddit=techssuport)
        """
        # Remove pre existing queries
        self.remove_query()
        # Concat all provided queries with a "&"
        query = "&".join([f"{key}={kwargs[key]}" for key in kwargs])
        self.url += "?" + query



    def remove_query(self):
        """
        Remove query paramter from the API Endpoint
        """
        self.url = self.url.split("?")[0]



    def add_paths(self, *args):
        """
        Add additional path(s) to the API Endpoint (e.g. base_url/{id})

        Args:
            *args (list) : a list of all path paramters
        """
        # Remove pre existing paths
        self.remove_paths()
        # Concat all provided paths with a "/"
        paths = "/".join(args)
        # Check if the current url contains queries at the end
        url_parts = self.url.split("?")
        if len(url_parts) == 2:
            # add paths between base_url and query
            self.url = url_parts[0] + "/" + paths + "?" + url_parts[1]
        else:
            # add paths to the end of the url
            self.url += "/" + paths



    def remove_paths(self):
        """
        Remove added paths from the url
        """
        # Check if the current url contains queries at the end
        url_parts = self.url.split("?")
        if len(url_parts) == 2:
            # Remove added paths while remain the queries
            self.url = self.base_url + "?" + url_parts[1]
        else:
            # overwrite var with the base_url
            self.url = self.base_url



    def remove_params(self):
        """
        Remove added paths & queries from the url
        """
        self.url = self.base_url



    def request(self) -> Optional[requests.Response.json]:
        """
        Make a request of the current url

        Return:
            response (dict) : response if status code was 200 | else None
        """
        response = requests.get(self.url)
        if self.check_response(response):
            return response.json()
        else:
            return None



    def check_response(self, response: requests.Response) -> bool:
        """
        Check the status code of the response

        Args:
            response (requests.Response) : response of the request

        Return:
            (bool) : True if status_code == 200 | else False
        """
        print(f"[INFO] - Status Code: {response.status_code} | Request: {self.url}")
        if response.status_code == 200:
            return True
        else:
            return False



    def get_base(self) -> str:
        return self.base_url



    def get_url(self) -> str:
        return self.url