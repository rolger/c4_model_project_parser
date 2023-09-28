
from structurizr import Workspace
from structurizr.model import Container, Location, Component

def write_dsl(workspace: Workspace):
    # Write the corresponding DSL code to the output file
    with open("./structurizr.dsl", "w") as f:
        f.write(format_indent(0, f'workspace "{workspace.name}" "{workspace.description}" {{\n'))
        f.write(format_indent(4, 'model {\n'))

        for software_system in workspace.model.software_systems:
            f.write(format_indent(8, f's{software_system.id} = softwaresystem "{software_system.name}" "{software_system.description}" {{\n'))

            for container in sorted(software_system.containers, key=lambda x: int(x.id)):
                f.write(format_indent(12, f'c{container.id} = container "{container.name}" "{container.description}" "{container.technology}" {{\n'))

                for component in container.components:
                    f.write(format_indent(16, f'c{component.id} = component "{component.name}" "{component.description}" "{component.technology}"'))
                    if "Interface" in component.tags:
                        f.write(format_indent(16, '{\n'))
                        f.write(format_indent(19,'tags "Interface" \n'))
                        f.write(format_indent(16,'}'))
                    f.write(format_indent(16, '\n'))
                f.write(format_indent(12, '}\n'))
                            
        f.write(format_indent(8, '}\n'))
        f.write(format_indent(8, '# relationships to/from components\n'))
        for software_system in workspace.model.software_systems:
            for container in sorted(software_system.containers, key=lambda x: int(x.id)):
                for component in container.components:
                    for relationship in component.relationships:
                        f.write(format_indent(8, f'c{relationship.source_id} -> c{relationship.destination_id} "Uses"\n'))

        f.write(format_indent(4, '}\n'))
        f.write(create_views(workspace))
        f.write(format_indent(0, '}\n'))
        f.close()

def create_views(workspace:Workspace):
    return f"""
    views {{
        systemlandscape "SystemLandscape" {{
            include *
        }}
{create_system_views(workspace.model.software_systems)}
{create_container_views(workspace.model.software_systems)}
{create_component_views(workspace.model.software_systems)}

        styles {{
            element "Component" {{
                background #3CBD11
                color #ffffff
                shape RoundedBox
            }}

            element "Interface" {{
                background #1D520B
                color #ffffff
                shape Circle
            }}
        }}

        theme default

    }}
""" 

def create_system_views(systems):
    view  = '\n'
    for software_system in systems:
        view = view + create_view_for(f's{software_system.id}', "systemcontext", "SystemContext")
    return view

def create_container_views(systems):
    view  = '\n'
    for software_system in systems:
        view = view + create_view_for(f's{software_system.id}', "container", "Containers")
    return view

def create_component_views(systems):
    view  = '\n'
    for software_system in systems:
        for container in sorted(software_system.containers, key=lambda x: int(x.id)):
            view = view + create_view_for(f'c{container.id}', "component", "")
    return view

def create_view_for(element_id, type, viewname):
    if viewname != "":
        t = f'"{viewname}"'
    else:
        t = ""

    return format_indent(8, f'{type} {element_id} {t} {{\n') + \
        format_indent(12, 'include *\n') + \
        format_indent(8, '}\n')
    
def format_indent(i, line):
    return f'{"": >{i}}{line}'
