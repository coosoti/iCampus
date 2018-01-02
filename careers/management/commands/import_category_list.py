from __future__ import unicode_literals
import xlrd

from django.utils.six.moves import range
from django.core.management.base import BaseCommand
from careers.models import Category

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3

import sys

if sys.version_info[0] >= 3:
    unicode = str
    
class Command(BaseCommand):
    help = (
        "Imports category from a local XLS file. "
        "Expects id, name, slug."
    )

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            "file_path",
            nargs=1,
            type=unicode,
        )

    def handle(self, *args, **options):
        verbosity = options.get("verbosity", NORMAL)
        file_path = options["file_path"][0]

        wb = xlrd.open_workbook(file_path)
        sh = wb.sheet_by_index(0)

        if verbosity >= NORMAL:
            self.stdout.write("=== Categories imported ===")
        for rownum in range(sh.nrows):
            if rownum == 0:
                # let's skip the column captions
                continue
            (id, name, slug) = sh.row_values(rownum)
            category, created = Category.objects.get_or_create(
                id=id,
                name=name,
                slug=slug,
            )
            if verbosity >= NORMAL:
                self.stdout.write("{}. {}".format(
                    rownum, category.name
            	))