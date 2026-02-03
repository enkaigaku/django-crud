from django.test.runner import DiscoverRunner


class ExistingDBTestRunner(DiscoverRunner):
    """
    Test runner that uses the existing database configuration without creating
    a separate test database. Useful for CI/CD pipelines where the DB is
    pre-populated via Docker Compose.
    """

    def setup_databases(self, **kwargs):
        """
        Skip test database creation.
        """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """
        Skip test database destruction.
        """
        pass
