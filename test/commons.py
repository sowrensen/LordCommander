import shelve
from os import makedirs, mkdir, path
from pathlib import Path
from shutil import rmtree


def generate_full_dummy_data():
    remove_test_files()
    testfile_directory = Path(__file__).parent.parent.resolve() / '.testfiles'
    project1_root = testfile_directory / 'project1'
    project2_root = testfile_directory / 'project2'
    makedirs(project1_root / 'pro1ins1', exist_ok=True)
    makedirs(project1_root / 'pro1ins2', exist_ok=True)
    makedirs(project2_root / 'pro2ins1', exist_ok=True)
    makedirs(project2_root / 'pro2ins2', exist_ok=True)
    data = {
        "active": "",
        "projects": {
            "project1": {
                "root": str(project1_root),
                "instances": ["pro1ins1", "pro1ins2"]
            },
            "project2": {
                "root": str(project2_root),
                "instances": ["pro2ins1", "pro2ins2"]
            }
        }
    }
    set_dummy_data(data)


def generate_dummy_data_with_no_instance():
    remove_test_files()
    testfile_directory = Path(__file__).parent.parent.resolve() / '.testfiles'
    project1_root = testfile_directory / 'project1'
    makedirs(project1_root)
    data = {
        "active": "project1",
        "projects": {
            "project1": {
                "root": str(project1_root),
                "instances": []
            }
        }
    }
    set_dummy_data(data)
    

def generate_dummy_data_with_one_instance():
    remove_test_files()
    (pro_path, pro_name, ins_name) = create_a_new_project()
    data = {
        "active": "project3",
        "projects": {
            pro_name: {
                "root": pro_path,
                "instances": [ins_name]
            }
        }
    }
    set_dummy_data(data)


def create_a_new_project():
    testfile_directory = Path(__file__).parent.parent.resolve() / '.testfiles'
    proj_name = 'project3'
    ins_name = 'pro3ins1'
    project3_root = testfile_directory / proj_name
    makedirs(project3_root / ins_name, exist_ok=True)
    return str(project3_root), str(proj_name), str(ins_name)


def get_test_shelve_file():
    if not path.exists('.testfiles'):
        mkdir('.testfiles')
    testdb = shelve.open('.testfiles/testdb', writeback=True)
    if not all(key in testdb.keys() for key in ['active', 'projects']):
        testdb['active'] = ''
        testdb['projects'] = {}
    return testdb


def set_dummy_data(data):
    testdb = get_test_shelve_file()
    testdb.clear()
    for key, value in data.items():
        testdb[key] = value
    close_db(testdb)
    
    
def close_db(db):
    db.close()


def remove_test_files():
    rmtree('.testfiles', ignore_errors=True)

