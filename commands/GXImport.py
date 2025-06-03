#! python3
import os
import Rhino
import System # type: ignore
from libs import gx_export_logic as gel
from libs import gx_config
from libs import filepicker

def main():
    print("**~~~~~~~~~~~~~~~~~~~**")
    print("Starting GeoXchange")

    doc = Rhino.RhinoDoc.ActiveDoc
    if not doc.Name:
        raise Exception("ERROR: Active file has no name. Save file first.")

    # Create a list of existing layers so they can be ignored later
    existing_layer_ids = set(layer.Id for layer in doc.Layers)

    # Pick and load dwg files from dialog
    dwg_filepaths = filepicker.pick_file(".dwg", "DWG Files")

    # Pick and load config file
    config = gx_config.GXConfig()
    transform = config.inverse_transform

    for file in dwg_filepaths:

        # Import DWG file
        rc = Rhino.RhinoApp.RunScript('_-Import "{}" _Enter'.format(file), False)
        if not rc:
            print("Failed to import DWG file.")
            return

        # Add parent layer
        parent_layer_name = os.path.basename(file)
        parent_layer = Rhino.DocObjects.Layer()
        parent_layer.Name = parent_layer_name
        parent_layer_index = doc.Layers.Add(parent_layer)
        if parent_layer_index < 0:
            print("Failed to create parent layer.")
            return
        parent_layer_id = doc.Layers[parent_layer_index].Id

        # Collect indices of newly imported layers and move them under the parent
        imported_layer_indices = []
        for layer in doc.Layers:
            if layer.Id not in existing_layer_ids and layer.ParentLayerId == System.Guid.Empty and layer.Name != parent_layer_name:
                layer.ParentLayerId = parent_layer_id
                doc.Layers.Modify(layer, layer.LayerIndex, True)
                imported_layer_indices.append(layer.LayerIndex)

        # Transform all objects on the imported layers
        for obj in doc.Objects:
            if obj.Attributes.LayerIndex in imported_layer_indices:
                geo = obj.Geometry.Duplicate()
                if geo and geo.Transform(transform):
                    doc.Objects.Replace(obj.Id, geo)

        doc.Views.Redraw()
        print("Imported layers from '{}' and transformed.".format(parent_layer_name))
        
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)