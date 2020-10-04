from colr import color

from lordcommander.controllers import ProjectController
from lordcommander.output import Output
from .commons import *


def test_empty_project_db(capsys):
    remove_test_files()
    testdb = get_test_shelve_file()
    pc = ProjectController(testdb)
    pc.view()
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("No project has been found in the list.", Output.DANGER) + "\n"


def test_adding_project_with_default_name(capsys):
    generate_full_dummy_data()
    (pro_path, pro_name, inst_name) = create_a_new_project()
    testdb = get_test_shelve_file()
    pc = ProjectController(testdb)
    pc.add(pro_path)
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("%s is added to project list." % pro_name, Output.SUCCESS) + "\n"


def test_adding_project_with_custom_name(capsys):
    generate_full_dummy_data()
    testdb = get_test_shelve_file()
    (pro_path, pro_name, inst_name) = create_a_new_project()
    custom_name = 'custom_proj'
    pc = ProjectController(testdb)
    pc.add(pro_path, name=custom_name)
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("%s is added to project list." % custom_name, Output.SUCCESS) + "\n"
    

def test_adding_existing_project(capsys):
    generate_full_dummy_data()
    testdb = get_test_shelve_file()
    existing_project_path = testdb['projects']['project1']['root']
    pc = ProjectController(testdb)
    pc.add(existing_project_path)
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("Project already exists!", Output.DANGER) + "\n"
    

def test_setting_invalid_project_as_active(capsys):
    generate_full_dummy_data()
    testdb = get_test_shelve_file()
    pc = ProjectController(testdb)
    pc.active('doesnotexists')
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("Project doesnotexists is not found in the list, to see available projects run 'proj "
                                 "view'.",
                        Output.DANGER) + "\n"


def test_setting_valid_project_as_active(capsys):
    generate_full_dummy_data()
    testdb = get_test_shelve_file()
    pc = ProjectController(testdb)
    pc.active('project2')
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("project2 is set as active project.", Output.SUCCESS) + "\n"


def test_removing_a_non_existing_project(capsys):
    generate_full_dummy_data()
    testdb = get_test_shelve_file()
    pc = ProjectController(testdb)
    pc.clear('project3')
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("Project is not found in the list.", Output.DANGER) + "\n"


def test_renaming_a_project(capsys):
    generate_full_dummy_data()
    testdb = get_test_shelve_file()
    pc = ProjectController(testdb)
    pc.rename('project2', 'custom_name')
    captured = capsys.readouterr()
    close_db(testdb)
    assert captured.out == color("Project project2 is renamed to custom_name.", Output.SUCCESS) + "\n"
