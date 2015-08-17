import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture
def web_driver(request):
    driver = webdriver.Remote(
        command_executor='http://hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)

    request.addfinalizer(driver.quit)
    return driver


def test_landslide_website_title(web_driver):
    web_driver.get('https://github.com/adamzap/landslide/')
    assert 'landslide' in web_driver.title


def test_pytest_website_title(web_driver):
    web_driver.get('http://pytest.org/latest/')
    assert 'helps you' in web_driver.title


def _test_local_app_title(web_driver):
    web_driver.get('http://web:5000')
    assert 'helps you' in web_driver.title
