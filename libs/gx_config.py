#! python3
import Rhino
import configparser
import rhinoscriptsyntax as rs # type: ignore
from libs import filepicker
from libs.constants import *

class GXConfig:
    def __init__(self):
        self.path = ""
        self.x = 0.00
        self.y = 0.00
        self.z = 0.00
        self.r = 0.00
        self.schema = ""
        self.header = ""
        self.transform = None
        self.inverse_transform = None

        try:
            self.pick_file()
        except Exception as e:
            print(e)
            exit(1)

        self.parse_file()
        self.construct_transforms()

    def pick_file(self):
        self.path = filepicker.pick_file(".ini", "Config File", YAK_SERVER)

    def parse_file(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        self.x = float(config.get("Transform", "x"))
        self.y = float(config.get("Transform", "y"))
        self.z = float(config.get("Transform", "z"))
        self.r = float(config.get("Transform", "r"))
        self.schema = config.get("Export", "Schema")
        self.header = config.get("Export", "Header")

    def construct_transforms(self):
        translation = (self.x, self.y, self.z)
        world_plane = rs.WorldXYPlane()
        rotate = rs.RotatePlane(world_plane, self.r, [0,0,1])
        move = rs.XformTranslation(translation)
        target_plane = rs.PlaneTransform(rotate,move)
        
        self.transform = rs.XformChangeBasis(target_plane,world_plane)
        self.inverse_transform = rs.XformChangeBasis(world_plane,target_plane)

    def get_header_layers(self):
        header_layers = []
        for layer in Rhino.RhinoDoc.ActiveDoc.Layers:
            layer_string = str(layer.FullPath)
            if layer_string.startswith(self.header):
                header_layers.append(layer)
        print(f"Header Layers: {header_layers}")
        return header_layers

    def get_header_objects(self,layers):
        objects = []
        for layer in layers:
            objs = Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(layer)
            if objs:
                objects.extend(objs)
        print(f"Object List: {objects}")
        return objects