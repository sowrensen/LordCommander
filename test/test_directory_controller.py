from colr import color

from lordcommander.controllers import DirectoryController
from lordcommander.output import Output
from .commons import *


def test_adding_an_instance(capsys):
    generate_dummy_data_with_no_instance()
    testdb = get_test_shelve_file()
    dc = DirectoryController(testdb['projects']['project1']['instances'])
    dc.add('pro1ins1')
    instances = testdb['projects']['project1']['instances']
    close_db(testdb)
    assert 'pro1ins1' in instances


def test_add_without_name(capsys):
    generate_dummy_data_with_no_instance()
    testdb = get_test_shelve_file()
    dc = DirectoryController(testdb['projects']['project1']['instances'])
    dc.add()
    captured = capsys.readouterr()
    assert captured.out == color("Aborting! No argument has been provided.", Output.DANGER) + "\n"
