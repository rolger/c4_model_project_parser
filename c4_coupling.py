from structurizr import Workspace
from structurizr.model import Component

def number_of_users(component: Component):
    internal = 0
    external = 0

    container = component.parent
    for rel in component.get_efferent_relationships():
        if rel.destination.parent == container:
            internal += 1
        else:
            external += 1
    
    return (internal, external)

def number_of_usages(component: Component):
    internal = 0
    external = 0

    container = component.parent
    for rel in component.get_afferent_relationships():
        if rel.source.parent == container:
            internal += 1
        else:
            external += 1
    return (internal, external)

def write_deps(workspace: Workspace):
    with open("./deps.csv", "w") as f:
        f.write('Container, Component, Internal Uses, External Uses, Internal Usage, External Usage\n')

        for software_system in workspace.model.software_systems:
            for container in sorted(software_system.containers, key=lambda x: int(x.id)):
                for component in container.components:
                    (uses_int, uses_ext) = number_of_users(component)
                    (used_int, used_ext) = number_of_usages(component)
                    f.write(f'{container.name}, {component.name}, {uses_int}, {uses_ext}, {used_int}, {used_ext}\n')
                    
        f.close()
