import os
import xml.etree.ElementTree as ET
from structurizr import Workspace
from structurizr.model import Container, Location, Component
from dataclasses import dataclass
from c4_coupling import write_deps
from c4_views import write_dsl

'''
    Create a C4 model from MS Visual Studio solution and project files.
    - Search for all soution paths inside a given directory: 
        get_solution_paths(directory)
    - Create a C4 workspace object with a given array of solution paths: 
        parse_dotnet_system(solution_paths)
    - Save the workspace to a DSL file which can be viewed with https://structurizr.com/dsl: 
        write_dsl(workspace)
'''

@dataclass
class ComponentData:
    name: str
    dotnet_project_path: str
    component: Component
    dependencies: set

def parse_maven_system(parent_pom_paths):
    # Create a Structurizr workspace
    workspace = Workspace(name="Automation Software", description="Software architecture for the automation software")

    # Create a model
    model = workspace.model

    # Level 1: Automation Software system
    automation_system = model.add_software_system(
        location=Location.Internal,
        name="Automation Software", 
        description="Main automation software system"
    )

    # Level 2: Parent poms with modules as containers with components
    for parent_pom_path in sorted(parent_pom_paths):
        # Parse the pom file
        tree = ET.parse(parent_pom_path)
        root_element = tree.getroot()
        xml_schema = root_element.tag.removesuffix("project")
            
        artifact = root_element.find(xml_schema + "artifactId")
        automation_system.add_container(artifact.text, "Maven container", "Java")

    return workspace


def get_parent_pom_paths(root_path, recursive=True, exclude = None):
    if recursive:
        file_iter = os.walk(root_path)
    else:
        file_iter =[next(os.walk(root_path))]

    solution_paths = []
    for root, dirs, files in file_iter:
        for file in files:
            if file.endswith("pom.xml") and (exclude == None or exclude not in file):
                with open(os.path.join(root, file), 'r') as f:
                    outputs = list(filter(lambda line: "<modules>" in line, f))
                    if len(outputs) == 1:
                        solution_paths.append(os.path.join(root, file))

    return solution_paths



# Example usage

parent_pom_paths = get_parent_pom_paths("C:/Users/rolandgerm/projects/lkww/DTM/dtm-bahn-faehre-cmp\\acceptance-tests")

workspace = parse_maven_system(parent_pom_paths)

print(workspace)
