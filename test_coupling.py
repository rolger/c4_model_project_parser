from structurizr import Workspace
from structurizr.model import Location, SoftwareSystem

from coupling import number_of_usages, number_of_users


def test_no_uses():
    workspace = Workspace(name="Software", description="Software architecture for software")
    model = workspace.model
    system =  model.add_software_system(
        location=Location.Internal,
        name="Software System", 
        description="Main automation software system"
    )

    container1 = system.add_container("A")
    c1 = container1.add_component(name="A.Impl")
    i1 = container1.add_component(name="A.Interface")

    container2 = system.add_container("B")
    c2 = container2.add_component(name="B.Impl")
    i2 = container2.add_component(name="B.Interface")

    (internal, external) = number_of_users(c1)
    
    assert 0 == internal
    assert 0 == external

def test_one_internal_uses():
    workspace = Workspace(name="Software", description="Software architecture for software")
    model = workspace.model
    system =  model.add_software_system(
        location=Location.Internal,
        name="Software System", 
        description="Main automation software system"
    )

    container1 = system.add_container("A")
    c1 = container1.add_component(name="A.Impl")
    i1 = container1.add_component(name="A.Interface")

    container2 = system.add_container("B")
    c2 = container2.add_component(name="B.Impl")
    i2 = container2.add_component(name="B.Interface")

    c1.uses(i1)

    (internal, external) = number_of_users(c1)
    
    assert 1 == internal
    assert 0 == external

def test_one_internal_and_one_external_uses():
    workspace = Workspace(name="Software", description="Software architecture for software")
    model = workspace.model
    system =  model.add_software_system(
        location=Location.Internal,
        name="Software System", 
        description="Main automation software system"
    )

    container1 = system.add_container("A")
    c1 = container1.add_component(name="A.Impl")
    i1 = container1.add_component(name="A.Interface")

    container2 = system.add_container("B")
    c2 = container2.add_component(name="B.Impl")
    i2 = container2.add_component(name="B.Interface")

    c1.uses(i1)
    c1.uses(i2)

    (internal, external) = number_of_users(c1)
    
    assert 1 == internal
    assert 1 == external

def test_used_by_none():
    workspace = Workspace(name="Software", description="Software architecture for software")
    model = workspace.model
    system =  model.add_software_system(
        location=Location.Internal,
        name="Software System", 
        description="Main automation software system"
    )

    container1 = system.add_container("A")
    c1 = container1.add_component(name="A.Impl")
    i1 = container1.add_component(name="A.Interface")

    container2 = system.add_container("B")
    c2 = container2.add_component(name="B.Impl")
    i2 = container2.add_component(name="B.Interface")

    (internal, external) = number_of_usages(c1)
    
    assert 0 == internal
    assert 0 == external

def test_used_by_one():
    workspace = Workspace(name="Software", description="Software architecture for software")
    model = workspace.model
    system =  model.add_software_system(
        location=Location.Internal,
        name="Software System", 
        description="Main automation software system"
    )

    container1 = system.add_container("A")
    c1 = container1.add_component(name="A.Impl")
    i1 = container1.add_component(name="A.Interface")

    container2 = system.add_container("B")
    c2 = container2.add_component(name="B.Impl")
    i2 = container2.add_component(name="B.Interface")

    c1.uses(i1)

    (internal, external) = number_of_usages(i1)
    
    assert 1 == internal
    assert 0 == external

def test_used_internal_and_external():
    workspace = Workspace(name="Software", description="Software architecture for software")
    model = workspace.model
    system =  model.add_software_system(
        location=Location.Internal,
        name="Software System", 
        description="Main automation software system"
    )

    container1 = system.add_container("A")
    c1 = container1.add_component(name="A.Impl")
    i1 = container1.add_component(name="A.Interface")

    container2 = system.add_container("B")
    c2 = container2.add_component(name="B.Impl")
    i2 = container2.add_component(name="B.Interface")

    c1.uses(i1)
    c2.uses(i2)
    i2.uses(i1)

    (internal, external) = number_of_usages(i1)
    
    assert 1 == internal
    assert 1 == external

def test_multiple_used_internal_and_external():
    workspace = Workspace(name="Software", description="Software architecture for software")
    model = workspace.model
    system =  model.add_software_system(
        location=Location.Internal,
        name="Software System", 
        description="Main automation software system"
    )

    container1 = system.add_container("A")
    c1 = container1.add_component(name="A.Impl")
    i1 = container1.add_component(name="A.Interface")

    container2 = system.add_container("B")
    c2 = container2.add_component(name="B.Impl")
    i2 = container2.add_component(name="B.Interface")

    c1.uses(i1)
    c2.uses(i2)
    i2.uses(i1)
    c2.uses(i1)

    (internal, external) = number_of_usages(i1)
    
    assert 1 == internal
    assert 2 == external
