import rhinoscriptsyntax as rs
import ConfigParser
import gx_functions as fun
import os
from System.IO import Path, File, FileInfo, FileAttributes

config = ConfigParser.RawConfigParser()
config.read('config.ini')

x = config.get('Transform','x')
y = config.get('Transform','y')
z = config.get('Transform','z')
r = config.get('Transform','r')

transform_out = fun.ConstructTransformation(x,y,z,r)
transform_in = fun.ConstructInverseTransform(transform_out)

rs.DocumentModified(False)

fname = rs.OpenFileName()

folder = Path.GetDirectoryName(fname)

rs.Command("_-Open " + chr(34) + fname + chr(34) + " _Enter", 0)
    
objs = rs.AllObjects()
    
rs.TransformObjects(objs, transform_in, False)
    
# Manually assign units to 'ft' without scaling
rs.UnitSystem(9, False)
    
out_name = folder + "\\" + Path.GetFileNameWithoutExtension(fname) + ".3dm"
rs.Command("_-SaveAs " + chr(34) + out_name + chr(34) + " _Enter",0)

rs.Command("_zoom _all _extents")