import argparse

import pytest
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs tests with Pytest"

    def add_arguments(self, parser):
        parser.add_argument("args", nargs=argparse.REMAINDER)

    def handle(self, *args, **options):
        pytest.main(list(args))
