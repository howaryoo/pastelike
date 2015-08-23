from flask import url_for


def test_landslide_website_title(web_driver):
    web_driver.get('https://github.com/adamzap/landslide/')
    assert 'landslide' in web_driver.title


def test_pytest_website_title(web_driver):
    web_driver.get('http://pytest.org/latest/')
    assert 'helps you' in web_driver.title


def test_local_app_title(test_client):
    test_client.get(url_for("hello"))
    from app import redis as main_redis
    hits_prev = int(main_redis.get('hits'))
    test_client.get(url_for("hello"))
    hits = int(main_redis.get('hits'))
    assert hits - hits_prev == 1, "Number of hits not incremented"
