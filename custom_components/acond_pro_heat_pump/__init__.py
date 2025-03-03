import aiohttp
from aiohttp import FormData
import ssl
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

class ExampleSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, value_key):
        super().__init__(coordinator)
        self._name = name
        self._value_key = value_key

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self.coordinator.data.get(self._value_key)

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    # Create a custom SSL context that doesn't verify certificates
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Create a cookie jar
    cookie_jar = aiohttp.CookieJar(unsafe=True)

    # Create the session with the cookie jar and custom SSL context
    session = async_create_clientsession(
        hass,
        cookie_jar=cookie_jar,
        verify_ssl=False,
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    )

    # Function to perform login and set cookies
    async def login():
        login_url = 'http://192.168.11.145/SYSWWW/LOGIN.XML'
        # login_data = {"username": "your_username", "password": "your_password"}
        response = await session.get(login_url)
        data = FormData(quote_fields=True, charset='utf-8')
        data.add_field('USER', 'PioLyc2024')
        data.add_field('PASS', 'PioLyc2024')
        response = await session.post(login_url, data=data)
            # The cookies from the response will be automatically stored in the cookie jar

    async def async_update_data():
        # Ensure we're logged in before making the request
        if not session.cookie_jar:
            await login()

        async with session.get("http://192.168.207.98/getParameters") as response:
            data = await response.json()
            return data["list"][0]

    coordinator = DataUpdateCoordinator(
        hass,
        hass.logger,
        name="example_sensor",
        update_method=async_update_data,
        update_interval=timedelta(minutes=5)
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        ExampleSensor(coordinator, "Vehicle State", "vehicleState"),
        ExampleSensor(coordinator, "EVSE State", "evseState"),
        ExampleSensor(coordinator, "Max Current", "maxCurrent"),
        ExampleSensor(coordinator, "Actual Current", "actualCurrent"),
        ExampleSensor(coordinator, "Actual Power", "actualPower")
    ]

    async_add_entities(sensors)
