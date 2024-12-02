from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        from coverage import Coverage

        cov = Coverage()
        cov.start()

        result = super().run_tests(test_labels, extra_tests, **kwargs)

        cov.stop()
        cov.save()
        cov.report()

        return result
