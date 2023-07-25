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
