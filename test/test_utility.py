import os

from colr import color

from lordcommander.output import Output
from lordcommander.utils import Utils
from .commons import *


def test_searching_a_instance(capsys):
    generate_dummy_data_with_one_instance()
    testdb = get_test_shelve_file()
    ut = Utils(testdb, testdb['projects']['project3'])
    ut.search('pro3ins1')
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("Found! Index: %d" % 0, Output.SUCCESS) + "\n"


def test_total(capsys):
    generate_dummy_data_with_one_instance()
    testdb = get_test_shelve_file()
    ut = Utils(testdb, testdb['projects']['project3'])
    ut.total()
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("Total %d directories listed." % 1, Output.INFO) + "\n"


def test_data_dump(capsys):
    generate_full_dummy_data()
    testfile_directory = Path(__file__).parent.parent.resolve() / '.testfiles'
    testdb = get_test_shelve_file()
    ut = Utils(testdb, testdb['projects']['project1'])
    ut.dump(testfile_directory)
    assert os.path.exists(testfile_directory / 'lcdb_dump.json')
