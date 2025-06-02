#! python3
import rhinoscriptsyntax as rs # type: ignore
import Rhino
import os

def get_initial_visibility(layers):
    initial_visibility = []
    for layer in layers:
        initial_visibility.append(layer.IsVisible)
    return initial_visibility
    
def turn_on_layers(layers):
    print(f"Layers: {layers}")
    for layer in layers:
        layer.IsVisible = True
        layer.CommitChanges()

def restore_layer_visibility(layers, initial_visibility):
    for i in range(0,len(layers)):
        layers[i].IsVisible = initial_visibility[i]
        layers[i].CommitChanges()

def export_dwg(DWGPath,schema):
    rs.Command(f'-Export "{DWGPath}" Scheme "{schema}" _Enter')

def export_layers_to_file(filePath,layers,objects,schema,transform):
    rs.EnableRedraw(False)
    
    # log visibility of export layers
    visibility = get_initial_visibility(layers)
    
    turn_on_layers(layers)
    
    moved_objects = []
    for object in objects:
        moved_objects.append(rs.TransformObject(object_id=object, matrix=transform, copy=True))
        
    rs.UnselectAllObjects()
    rs.SelectObjects(moved_objects)

    export_dwg(filePath,schema)
    
    for object in moved_objects:
        rs.DeleteObject(object)
    
    restore_layer_visibility(layers, visibility)

    rs.UnselectAllObjects()

    rs.EnableRedraw(True)

def ensure_export_folder(base_folder, sub_folder):
    # Debugging output
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"...checking for export folder...")
    print(f"Base Folder: {base_folder}, Sub Folder: {sub_folder}")

    # Define the path for the export subfolder
    export_folder = os.path.join(base_folder, sub_folder)
    
    # Check if the export folder exists and create if needed
    if not os.path.isdir(export_folder):
        os.makedirs(export_folder)
        print(f"Created directory {export_folder}")
    else:
        print(f"Directory {export_folder} already exists")
    print("~~~~~~~~~~~~~~~~~~~~~~~~")