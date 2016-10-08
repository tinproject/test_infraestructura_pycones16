import pytest
import requests


@pytest.mark.skip(reason="This won't work with vagrant because hostname handling")
def test__webserver_working(TestinfraBackend):
    host = TestinfraBackend.get_hostname()
    r = requests.get("http://" + host)
    assert r.status_code == 200


@pytest.mark.skip(reason="This won't work with vagrant because hostname handling")
def test__server_connection(LocalCommand, TestinfraBackend):
    host = TestinfraBackend.get_hostname()
    cmd = LocalCommand("ping -c 5 {}".format(host))
    assert cmd.rc == 0


def test__sentry_user(User):
    sentry = User("sentry")
    assert sentry.exists
    assert sentry.name == "sentry"
    assert sentry.uid < 1000
    assert sentry.group == "sentry"
    assert sentry.shell == "/sbin/nologin"


def test__sentry_group(Group):
    sentry_group = Group("sentry")
    assert sentry_group.exists


def test__sentry_database_exists(Sudo, Command):
    with Sudo("postgres"):
        cmd_str = """psql -d sentry -c "SELECT 1;" """
        cmd = Command(cmd_str)
        assert cmd.rc == 0


def test__sentry_config_folder(File):
    f = File("/etc/sentry")
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "sentry"
    assert f.mode == 0o755


@pytest.mark.parametrize("cfg_file", [
    "config.yml",
    "sentry.conf.py",
])
def test__sentry_config__files(File, cfg_file):
    f = File("/etc/sentry/%s" % cfg_file)
    assert f.is_file
    assert f.user == "root"
    assert f.group == "sentry"
    assert f.mode == 0o640


@pytest.mark.parametrize("txt", [
    "SENTRY_WEB_HOST = '127.0.0.1'",
    "SENTRY_WEB_PORT = 9000",
])
def test__sentry_config_values(txt, File, Sudo):
    with Sudo("sentry"):
        f = File("/etc/sentry/sentry.conf.py")
        assert f.contains(txt)


@pytest.mark.parametrize("pkg", [
    "python-setuptools", "python-pip", "python-dev",
    "libxslt1-dev", "gcc", "libffi-dev",
    "libjpeg-dev", "libxml2-dev", "libyaml-dev",
    # "libxslt-dev",  # This is a virtual package on Debian 8, apt installs libxslt1-dev instead.
    "clang",  # Not in specified sentry docs
])
def test__sentry_packages_prerequisites(Package, pkg):
    assert Package("{}".format(pkg)).is_installed


def test__redis_server_is_installed(Package):
    assert Package("redis-server").is_installed


def test__postgresql_is_installed(Package):
    pgsql = Package("postgresql-9.6")
    assert pgsql.is_installed
    assert pgsql.version >= "9.6"


def test__nginx_is_intalled(Package):
    assert Package("nginx").is_installed


@pytest.mark.parametrize("srv", [
    "redis-server",
    "postgresql",
    "nginx",
])
def test__req_services_are_running_and_enabled(Service, srv):
    assert Service(srv).is_running
    assert Service(srv).is_enabled


@pytest.mark.parametrize("srv", [
    "sentry-web",
    "sentry-worker",
    "sentry-cron",
])
def test__sentry_services_are_running_and_enabled(Service, srv):
    assert Service(srv).is_running
    assert Service(srv).is_enabled


def test__processes(Process):
    processes = Process.filter(uname="sentry")
    mem = sum((p.pmem for p in processes))
    assert mem < 40  # 40% of systems's memory


@pytest.mark.xfail(reason="IP could change")
def test__interface(Interface):
    eth = Interface("eth0")
    assert eth.exists
    assert "10.0.2.15" in eth.addresses


def test__postgres__is_listening(Socket):
    assert Socket("tcp://127.0.0.1:5432").is_listening


def test__redis__is_listening(Socket):
    assert Socket("tcp://127.0.0.1:6379").is_listening


def test__sentry__is_listening(Socket):
    assert Socket("tcp://127.0.0.1:9000").is_listening


def test__nginx__is_listening(Socket):
    assert Socket("tcp://0.0.0.0:80").is_listening


def test__system_info(SystemInfo):
    assert SystemInfo.distribution == 'debian'
    assert SystemInfo.codename == 'jessie'
    assert SystemInfo.release == '8.6'


def test__all_is_working():
    r = requests.get("http://localhost:8080")
    assert r.status_code == 200
    assert 'sentry' in r.text
