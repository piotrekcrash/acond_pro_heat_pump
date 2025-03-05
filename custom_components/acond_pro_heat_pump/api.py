"""Sample API Client."""

from __future__ import annotations
import socket
from typing import Any
from .const import LOGGER
import aiohttp
import ssl
import async_timeout
from bs4 import BeautifulSoup
from .const import URL_LOGIN, URL_HOME

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class AcondProApiClientError(Exception):
    """Exception to indicate a general API error."""


class AcondProApiClientCommunicationError(
    AcondProApiClientError,
):
    """Exception to indicate a communication error."""


class AcondProApiClientAuthenticationError(
    AcondProApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise AcondProApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class AcondProApiClient:
    """Sample API Client."""

    def __init__(
        self,
        ip_address: str,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._ip_address = ip_address
        self._username = username
        self._password = password
        self._session = session
        # self._session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True), connector=aiohttp.TCPConnector(ssl=ssl_context))

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )
    
    async def async_get_home(self) -> Any:
        LOGGER.error('LOAD_DATA')
        response = await self._api_txt_wrapper(
            method="get",
            url='',
        )
        return response

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise AcondProApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise AcondProApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise AcondProApiClientError(
                msg,
            ) from exception
    
    async def login(self) -> Any:
        """Get data from the API."""
        LOGGER.error('LOGIN')
        login_url = "https://" + self._ip_address + URL_HOME
        response = await self._api_txt_wrapper(
            method="get",
            url=login_url,
        )

    def map_response(self, strResponse) -> Any:
        soup = BeautifulSoup(strResponse, 'lxml-xml')
        input_elements = soup.find_all('INPUT')
        value_dict = {}
        for input_elem in input_elements:
            name = input_elem.get('NAME')
            value = input_elem.get('VALUE')
            value_dict[name] = value
        return value_dict
    
    def login_form(self) -> aiohttp.FormData:
        data = aiohttp.FormData(quote_fields=True, charset='utf-8')
        data.add_field("USER", self._username)
        data.add_field("PASS", self._password)
        return data

    async def _api_txt_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                sess = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True), connector=aiohttp.TCPConnector(ssl=ssl_context))
                # cookie_jar = aiohttp.CookieJar(unsafe=True)
                # async with aiohttp.ClientSession(cookie_jar=cookie_jar, connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                async with sess as session:
                    await session.get("https://" + self._ip_address + URL_LOGIN)
                    response = await session.post(url="https://" + self._ip_address + URL_LOGIN, data=self.login_form())
                    body = await response.read()
                    strBody = body.decode('utf-8', errors='replace')
                    return self.map_response(strBody)
        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise AcondProApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise AcondProApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise AcondProApiClientError(
                msg,
            ) from exception
