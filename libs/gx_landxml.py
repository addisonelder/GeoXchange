#! python3
import rhinoscriptsyntax as rs #type: ignore
import Rhino
import Rhino.Geometry as rg
import Eto.Forms as forms
import Rhino.UI as ui
import xml.etree.ElementTree as ET
import re
import math
import System # type: ignore
from libs import filepicker
from libs.constants import *
from libs import gx_geometry

class LandXML():
    def __init__(self):
        self.path = None
        self.tree = None
        self.root = None
        self.ns = None

        self.alignment = None

        try:
            self.pick_file()
            print("pickfile_success")
        except Exception as e:
            print(e)

        self.parse_as_tree()
        print("parse_success")

    def pick_file(self):
        self.path = filepicker.pick_file(".xml", "LandXML Files")

    def parse_as_tree(self):
        # Set XML tree and root
        self.tree = ET.parse(self.path)
        print(self.tree)
        self.root = self.tree.getroot()
        print(self.root)

        # Extract the default namespace from the root tag
        # (format: {namespace}tag)
        m = re.match(r'\{(.*)\}', self.root.tag)
        namespace = m.group(1) if m else ''

        # Build the namespace dictionary for ElementTree search
        self.ns = {'ns': namespace} if namespace else {}
        print(self.ns)

class Alignment():
    def __init__(self, landxml):
        self.landxml = landxml
        self.name = None
        self.start_sta = None
        self.lines = None
        self.curves = None
        self.polycurve = None

        self.extract_alignment_data()
        self.extract_lines()
        self.extract_curves()

    def extract_alignment_data(self):
        for alignment in self.landxml.root.findall('.//ns:Alignment', self.landxml.ns):
            #Find Parameters
            self.name = alignment.get('name')
            self.start_sta = float(alignment.get('staStart'))

    def extract_lines(self):
        line_list = []
        for entry in self.landxml.root.findall('.//ns:Line', self.landxml.ns):
            start = self.parse_point(entry, "Start")
            end = self.parse_point(entry, "End")
            line = rg.Line(start, end)
            line = line.ToNurbsCurve()
            line_list.append(line)
        self.lines = line_list
            
    def extract_curves(self):
        curve_list = []
        for entry in self.landxml.root.findall('.//ns:Curve', self.landxml.ns):
            # pull parameters from landxml
            start = self.parse_point(entry, "Start")
            end = self.parse_point(entry, "End")
            center = self.parse_point(entry, "Center")
            radius = float(entry.get('radius'))
            direction = entry.get('rot')

            # build the arc
            circle = rg.Circle(center,radius)
            circle = circle.ToNurbsCurve()
            start_param = circle.ClosestPoint(start)[1]
            end_param = circle.ClosestPoint(end)[1]
            if direction == "ccw":
                domain = rg.Interval(start_param,end_param)
            else:
                domain = rg.Interval(end_param,start_param)
            
            arc = circle.Trim(domain)
            curve_list.append(arc)
        self.curves = curve_list

    def parse_point(self, item, search):
        # pull a point item from an XML branch
        point_string = item.find(f'ns:{search}', self.landxml.ns).text.strip()
        y_str, x_str = point_string.split()
        x = float(x_str)
        y = float(y_str)
        point = rg.Point3d(x,y,0)
        return point
