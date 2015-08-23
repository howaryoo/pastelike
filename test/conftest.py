import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from app import create_app


# Flask fixtures
@pytest.yield_fixture(scope="session")
def app():
    """
    Creates a new Flask application for a test duration.
    Uses application factory `create_app`.
    """
    _app = create_app()
    _app.testing = True

    yield _app

    # TODO add teardown code


@pytest.fixture(scope="function")
def test_client(app):
    return app.test_client()


# Selenium fixtures
@pytest.fixture
def web_driver(request):
    driver = webdriver.Remote(
        command_executor='http://hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)

    request.addfinalizer(driver.quit)
    return driver
