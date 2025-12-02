"""Sample API Client."""

from __future__ import annotations
import socket
from typing import Any
from .const import LOGGER, URL_LOGIN, URL_HOME
import aiohttp
import ssl
import async_timeout
from bs4 import BeautifulSoup

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

HTTP_FOUND = 302


class AcondProApiClientError(Exception):
    """Exception to indicate a general API error."""


class AcondProApiClientCommunicationError(AcondProApiClientError):
    """Exception to indicate a communication error."""


class AcondProApiClientAuthenticationError(AcondProApiClientError):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise AcondProApiClientAuthenticationError(msg)
    response.raise_for_status()


class AcondProApiClient:
    """Sample API Client."""

    def __init__(self,
        ip_address: str,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._ip_address = ip_address
        self._username = username
        self._password = password
        self._cookie_jar = aiohttp.CookieJar(unsafe=True)
        self._session = session

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
        LOGGER.error("LOAD_DATA")
        response = await self._api_txt_wrapper(
            method="get",
            url=URL_HOME,
        )
        return response

    async def async_set_value(self, name: str, value: str) -> Any:
        LOGGER.error("SET_VALUE")
        response = await self._api_txt_wrapper(
            method="post",
            url=URL_HOME,
            data=self.value_update_form(name, value),
        )
        LOGGER.error(response)
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
            raise AcondProApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise AcondProApiClientCommunicationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise AcondProApiClientError(msg) from exception

    async def login(self) -> Any:
        """Get data from the API."""
        LOGGER.error("LOGIN")
        await self._api_txt_wrapper(
            method="get",
            url=URL_HOME,
        )

    def map_response(self, str_response: str) -> Any:
        soup = BeautifulSoup(str_response, "lxml-xml")
        input_elements = soup.find_all("INPUT")
        value_dict: dict[str, str | None] = {}
        for input_elem in input_elements:
            name = input_elem.get("NAME")
            value = input_elem.get("VALUE")
            value_dict[name] = value
        return value_dict

    def login_form(self) -> aiohttp.FormData:
        data = aiohttp.FormData(quote_fields=True, charset="utf-8")
        data.add_field("USER", self._username)
        data.add_field("PASS", self._password)
        return data

    def value_update_form(self, name: str, value: str) -> aiohttp.FormData:
        data = aiohttp.FormData(quote_fields=True, charset="utf-8")
        data.add_field(name, value)
        return data

    def _build_url(self, url: str) -> str:
        return "https://" + self._ip_address + url

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
                async with aiohttp.ClientSession(
                    cookie_jar=self._cookie_jar,
                    connector=aiohttp.TCPConnector(ssl=ssl_context),
                ) as session:
                    response = await session.request(
                        url=self._build_url(url),
                        method=method,
                        data=data,
                        headers=headers,
                        allow_redirects=False,
                    )
                    if response.status == HTTP_FOUND:
                        LOGGER.error("AUTH after 302")
                        response = await session.post(
                            url=self._build_url(URL_LOGIN),
                            data=self.login_form(),
                            allow_redirects=False,
                        )
                        if (
                            response.status == HTTP_FOUND
                            and response.headers.get("Location") == URL_LOGIN
                        ):
                            LOGGER.error("302 after AUTH")
                            msg = "Invalid credentials"

                            def _raise_auth_error(message: str) -> None:
                                raise AcondProApiClientAuthenticationError(message)

                            _raise_auth_error(msg)
                    response = await session.request(
                        url=self._build_url(url),
                        method=method,
                        data=data,
                        headers=headers,
                        allow_redirects=False,
                    )
                    body = await response.read()
                    str_body = body.decode("utf-8", errors="replace")
                    return self.map_response(str_body)
        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise AcondProApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise AcondProApiClientCommunicationError(msg) from exception
        except AcondProApiClientAuthenticationError as exception:
            msg = f"Invalid credentials - {exception}"
            raise AcondProApiClientAuthenticationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise AcondProApiClientError(msg) from exception
