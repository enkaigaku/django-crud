from django.apps import apps
from django.test.runner import DiscoverRunner


class ManagedModelTestRunner(DiscoverRunner):
    """
    Test runner that forces all models to be managed=True during testing.
    This allows Django to create tables for models that are normally managed=False
    (e.g. legacy database models).
    """

    def setup_test_environment(self, *args, **kwargs):
        super().setup_test_environment(*args, **kwargs)
        self.unmanaged_models = []
        # Loop through all models and force managed=True
        for model in apps.get_models():
            if not model._meta.managed:
                model._meta.managed = True
                self.unmanaged_models.append(model)

    def teardown_test_environment(self, *args, **kwargs):
        super().teardown_test_environment(*args, **kwargs)
        # Revert managed status
        for model in self.unmanaged_models:
            model._meta.managed = False
