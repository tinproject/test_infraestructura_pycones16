import pytest
import requests

pytestmark = pytest.mark.skipif(True, reason="Don't hit my blog everytime tests run!")

def test_blog_landing_page_ok():
    r = requests.get('http://agus.tinproject.es')
    assert r.status_code == 200


def blog_article_page_ok_test():
    r = requests.get('http://agus.tinproject.es/2013/02/14/entendiendo-gescal/')
    assert r.status_code == 200


def test__category_permalinks__ok():
    r = requests.get('http://agus.tinproject.es/category/gis/')
    assert r.status_code == 200


def calendar_month_permalinks__ok__test():
    r = requests.get('http://agus.tinproject.es/2010/12/')
    assert r.status_code == 200


def test__admin_page__redirects():
    r = requests.get('http://agus.tinproject.es/admin')
    assert r.status_code == 200


@pytest.mark.parametrize("url, status", [
    ("agus.tinproject.es", 200),
    ("agus.tinproject.es/2013/02/14/entendiendo-gescal/", 200),
    ("agus.tinproject.es/category/gis", 200),
    ("agus.tinproject.es/2010/12/", 200),
    ("agus.tinproject.es/admin", 200),
])
def test__blog_urls(url, status):
    r = requests.get('http://{}'.format(url))
    assert r.status_code == status


@pytest.fixture()
def blog():
    class Client:
        def __init__(self):
            self.scheme = "http"
            self.host = "agus.tinproject.es"

        def get(self, location, **kwargs):
            url = "{}://{}{}".format(self.scheme, self.host, location)
            return requests.get(url, allow_redirects=False, **kwargs)

    return Client()


@pytest.mark.parametrize("endpoint, status", [
    ("/", 200),
    ("/category/gis", 301),
    ("/admin", 302),
])
def test__blog_endpoints(endpoint, status, blog):
    r = blog.get(endpoint)
    assert r.status_code == status
