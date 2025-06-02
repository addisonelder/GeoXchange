#! python3
import System # type: ignore
import Rhino
import Eto.Forms as forms # type: ignore
import Rhino.UI as ui
import configparser
import rhinoscriptsyntax as rs # type: ignore


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
        self.header_layers = []

        try:
            self.pick_file()
        except Exception as e:
            print(e)
            exit(1)

        self.parse_file()
        self.construct_transform()
        self.construct_inverse_transform()
        #self.find_header_layers

    def pick_file(self):
        dialog = forms.OpenFileDialog()
        dialog.Filters.Add(forms.FileFilter("Config Files (*.ini)", [".ini"]))
        dialog.Filters.Add(forms.FileFilter("All Files (*.*)", ["*"]))
        dialog.FilterIndex = 0  # explicitly select first filter
        dialog.Directory = System.Uri("//omapi-fs01/PA-WV Bridge Storage/Yak/GeoXchange_Configs")

        if dialog.ShowDialog(ui.RhinoEtoApp.MainWindow) == forms.DialogResult.Ok:
            selected_files = dialog.Filenames
            # Process the selected files
            for file_path in selected_files:
                print(f"Opening Config File: {file_path}")
            self.path = file_path
        else:
            raise Exception("ERROR: Invalid file, or no file was selected")

    def parse_file(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        self.x = float(config.get("Transform", "x"))
        self.y = float(config.get("Transform", "y"))
        self.z = float(config.get("Transform", "z"))
        self.r = float(config.get("Transform", "r"))
        self.schema = config.get("Export", "Schema")
        self.header = config.get("Export", "Header")

    def construct_transform(self):
        translation = (self.x, self.y, self.z)
        world_plane = rs.WorldXYPlane()
        rotate = rs.RotatePlane(world_plane, self.r, [0,0,1])
        move = rs.XformTranslation(translation)
        target_plane = rs.PlaneTransform(rotate,move)
        
        self.transform = rs.XformChangeBasis(target_plane,world_plane)

    def construct_inverse_transform(self):
        self.inverse_transform = rs.XformInverse(self.transform)

    def get_header_layers(self):
        all_file_layers = []
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