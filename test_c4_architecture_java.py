from structurizr import Workspace
from structurizr.model import Container, Location, Component
from c4_architecture_java import get_parent_pom_paths, parse_maven_system

def test_no_modules():
    solution_paths = get_parent_pom_paths("C:/Users/rolandgerm/projects/lkww/DTM/dtm-bahn-faehre-cmp\\acceptance-tests")
    assert len(solution_paths) == 0

def test_pom_file_contains_modules():
    solution_paths = get_parent_pom_paths("C:/Users/rolandgerm/projects/lkww/DTM/dtm-bahn-faehre-cmp")
    assert solution_paths[0].endswith("pom.xml")

def test_parse_container_named_pom_artifactid():
    workspace = parse_maven_system(["C:/Users/rolandgerm/projects/lkww/DTM/dtm-bahn-faehre-cmp/pom.xml"])

    for software_system in workspace.model.software_systems:
        for container in sorted(software_system.containers, key=lambda x: int(x.id)):
            assert container.name == "dtm-bahn-faehre-cmp"