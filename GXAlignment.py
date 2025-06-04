#! python3
# flag: python.reloadEngine

import Rhino
from libs import gx_landxml

import traceback

def main():

    print("**~~~~~~~~~~~~~~~~~~~**")
    print("Starting GeoXchange")

    active_doc = Rhino.RhinoDoc.ActiveDoc
    if not active_doc.Name:
        raise Exception("ERROR: Active file has no name. Save file first.")

    # Load config file
    xml_file = gx_landxml.LandXML()

    #print(xml_file)
    print(f"Root: {xml_file.root}")
    print(type(f"Tree: {xml_file.tree}"))

    alignment = gx_landxml.Alignment(xml_file)
    a = alignment.extract_alignment_data()
    print(f"Alignment Name: {alignment.name}")
    print(f"Alignment Start Station: {alignment.start_sta}")

    print(f"Lines: {alignment.lines}")
    print(f"Curves: {alignment.curves}")



if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())