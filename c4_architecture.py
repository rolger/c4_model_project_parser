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

def parse_dotnet_system(solution_paths, reference_keyword = "<Reference"):
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

    # Level 2: Solutions with Projects as containers with components
    all_project_components = {}
    for solution_path in sorted(solution_paths):
        solution_name = os.path.splitext(os.path.basename(solution_path))[0]
        solution_container = automation_system.add_container(solution_name, "Solution container", ".NET")

        all_project_components |= parse_dotnet_projects(solution_path, solution_container)
        all_project_components |= parse_cplusplus_projects(solution_path, solution_container)


    for project in all_project_components:
        dependencies = get_project_dependencies(all_project_components[project].dotnet_project_path, reference_keyword)
        all_project_components[project].dependencies = dependencies
        for dependency_name in dependencies:
            for project_key in all_project_components:
                if all_project_components[project_key].name == dependency_name:
                    all_project_components[project].component.uses(all_project_components[project_key].component, "Uses")
    
    return workspace


def get_solution_paths(root_path, recursive=True, exclude = None):
    if recursive:
        file_iter = os.walk(root_path)
    else:
        file_iter =[next(os.walk(root_path))]

    solution_paths = []
    for root, dirs, files in file_iter:
        for file in files:
            if file.endswith(".sln") and (exclude == None or exclude not in file):
                solution_paths.append(os.path.join(root, file))

    return solution_paths


def parse_dotnet_projects(solution_path, container: Container):
    project_file_names = get_project_file_names(solution_path)

    # Dictionary
    all_projects = {}

    for project_path in project_file_names:
        project_name, output_type_element = parse_dotnet_project_file(project_path)
        if "Test" not in project_path and "Test" not in project_name:
            component = container.add_component(name=project_name, description="Project component", technology=f"C# {output_type_element}")
            if "Interface" in project_name:
                component.tags.add("Interface")
            all_projects[project_name] = ComponentData(name=project_name, dotnet_project_path=project_path, component=component, dependencies=[])

    return all_projects

def parse_cplusplus_projects(solution_path, container: Container):
    project_file_names = get_project_file_names(solution_path, ".vcxproj")

    # Dictionary
    all_projects = {}

    for project_path in project_file_names:
        project_name, output_type_element = parse_cplusplus_project_file(project_path)
        if "Test" not in project_path and "Test" not in project_name:
            component = container.add_component(name=project_name, description="Project component", technology=f"C++ {output_type_element}")
            all_projects[project_name] = ComponentData(name=project_name, dotnet_project_path=project_path, component=component, dependencies=[])

    return all_projects

def get_project_file_names(solution_path, project_extension = ".csproj"):
    project_file_names = []
    
    with open(solution_path, "r") as f:
        for line in f:
            if line.strip().startswith("Project"):
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    project_name = parts[1].strip().strip('"')
                    project_directory = os.path.dirname(os.path.abspath(solution_path))
                    project_full_name = os.path.join(project_directory, project_name)
                    if project_name.endswith(project_extension) and os.path.isfile(project_full_name):
                        project_file_names.append(project_full_name)

    return project_file_names

def parse_cplusplus_project_file(project_path):
    project_name = project_name = os.path.splitext(os.path.basename(project_path))[0]

    with open(project_path, 'r') as f:
        outputs = list(filter(lambda line: "<ConfigurationType>" in line, f))

    output_type = 'DLL' if 'DynamicLibrary' in outputs[0] else 'EXE'
    return project_name, output_type

def parse_dotnet_project_file(project_path):
    # Parse the .csproj file
    tree = ET.parse(project_path)
    root_element = tree.getroot()
    xml_schema = root_element.tag.removesuffix("Project")

    property_group = root_element.find(xml_schema + "PropertyGroup")

    assembly_name_element = property_group.find(xml_schema + "AssemblyName")
    if assembly_name_element is not None and assembly_name_element.text:
        project_name = assembly_name_element.text
    else:
        # Use file name if assembly name not found
        project_name = os.path.splitext(os.path.basename(project_path))[0]

    output_type = property_group.find(xml_schema + "OutputType")
    if output_type is not None and output_type.text:
        output_type = output_type.text
    else:
        output_type = ''

    return project_name, output_type

def get_project_dependencies_via_xml(project_path):
    # Parse the .csproj file
    tree = ET.parse(project_path)
    root_element = tree.getroot()

    # Get the project references
    references = root_element.findall("{http://schemas.microsoft.com/developer/msbuild/2003}ItemGroup/{http://schemas.microsoft.com/developer/msbuild/2003}Reference")
    
    # Add dependencies to the component_dependencies dictionary
    dependencies = []
    if references:
        for reference in references:
            ref_include = reference.get("Include")
            dependencies.append(ref_include)

    return set(dependencies)


def get_project_dependencies(project_path, reference_keyword):
    dependencies = []
    with open(project_path, "r") as f:
        for line in f:
            if line.strip().startswith(f"{reference_keyword} Include"):
                if reference_keyword == "<Reference":
                    dependency_path = line.split('"')[1].split(',')[0]
                else:
                    dependency_path = line.split('"')[1].split('\\')[1]

                dependencies.append(dependency_path)
    return set(dependencies)

# Example usage

'''
    solution_paths = get_solution_paths"C:/Users/rolandgerm/projects/admiral/asw.betting.svc.engine"
    solution_paths = get_solution_paths"C:/Users/rolandgerm/projects/admiral/admiral.programengine"

    solution_paths = get_solution_paths"C:/Users/rolandgerm/projects/icagile-prg-archive/icagile-prg-admiral-2022/SupermarketReceipt-Refactoring-Kata/csharp"
    you can run it with different dependencies
    solution_paths = parse_dotnet_system(root_path, "<ProjectReference")

    solution_paths = get_solution_paths("C:/Users/rolandgerm/projects/BuR")

    base_dir = "C:/Users/rolandgerm/source/Workspaces/ASW/AutomationStudio/Trunk/"
solution_paths = get_solution_paths(base_dir + "Subsystems")
solution_paths += get_solution_paths(base_dir, False)

solution_paths = get_solution_paths(base_dir + "Subsystems", True, "Interfaces.sln")
solution_paths =  [base_dir + "Subsystems/Interfaces.sln"]
workspace = parse_dotnet_system(solution_paths, "<Reference")
'''

base_dir = "C:/Users/rolandgerm/source/AutomationStudio/"
solution_paths = get_solution_paths("C:/Users/rolandgerm/projects/icagile-prg-archive/icagile-prg-admiral-2022/SupermarketReceipt-Refactoring-Kata/csharp")
solution_paths = get_solution_paths("C:/Users/rolandgerm/projects/admiral/asw.betting.svc.engine")
workspace = parse_dotnet_system(solution_paths, "<ProjectReference")

solution_paths =  [base_dir + "Subsystems/Interfaces.sln"]
solution_paths = get_solution_paths(base_dir + "Subsystems", True)
workspace = parse_dotnet_system(solution_paths, "<Reference")

write_deps(workspace)
write_dsl(workspace)
