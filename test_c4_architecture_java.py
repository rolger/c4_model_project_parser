from unittest import mock
from unittest.mock import mock_open, patch
from structurizr import Workspace
from structurizr.model import Container, Location, Component
from c4_architecture_java import get_parent_pom_paths, parse_maven_system

def test_no_modules():
    with mock.patch('os.walk') as mockwalk:
        mockwalk.return_value = [
            ('/foo', ('bar',), ('baz',))
        ]

        solution_paths = get_parent_pom_paths("/anydir")

    assert len(solution_paths) == 0

def test_pom_file_contains_modules():
    with mock.patch('os.walk') as mockwalk:
        mockwalk.return_value = [
            ('/foo', ('bar',), ('pom.xml',))
        ]

        with mock.patch('builtins.open', mock.mock_open(read_data='<modules></modules>')):
            solution_paths = get_parent_pom_paths("/anydir")

    assert solution_paths[0] == "/foo\\pom.xml"

@patch('builtins.open', new_callable=mock.mock_open, read_data=
        '''
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <parent>
                <artifactId>parent-id</artifactId>
            </parent>
            <artifactId>test-id</artifactId>
        </project>
        ''')
def test_parse_container_named_pom_artifactid(fake_file):
    workspace = parse_maven_system(["pom.xml"])

    for software_system in workspace.model.software_systems:
        for container in sorted(software_system.containers, key=lambda x: int(x.id)):
            assert container.name == "test-id"