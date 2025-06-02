#! python3
import os
import Rhino
from libs import gx_export_logic as gel
from libs import gx_config

def main():

    print("**~~~~~~~~~~~~~~~~~~~**")
    print("Starting GeoXchange")

    active_doc = Rhino.RhinoDoc.ActiveDoc
    if not active_doc.Name:
        raise Exception("ERROR: Active file has no name. Save file first.")

    # Load config file
    config = gx_config.GXConfig()

    # Get layers and objects from header
    layers = config.get_header_layers()
    objects = config.get_header_objects(layers)
    if not objects:
        raise Exception(f'ERROR: No objects found under parent layer "{config.header}"')

    # Create export folder if needed
    path = os.path.dirname(active_doc.Path)
    subfolder = "export"
    gel.ensure_export_folder(path, subfolder)

    # Perform transformation and export
    dwg_name = str(active_doc.Name).replace("3dm", "dwg")
    file_path = f"{path}\{subfolder}\export_{dwg_name}"
    print(f"Export File Path: {file_path}")
    gel.export_layers_to_file(file_path, layers, objects, config.schema, config.transform)

    print("GeoXchange export ran successfully")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)