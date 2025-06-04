from libs.constants import *
import Eto.Forms as forms
import Rhino.UI as ui
import System #type: ignore

def pick_file(extension, description, directory=None):
    dialog = forms.OpenFileDialog()
    dialog.Filters.Add(forms.FileFilter(f"{description} (*{extension})", [f"{extension}"]))
    dialog.Filters.Add(forms.FileFilter("All Files (*.*)", ["*"]))
    dialog.FilterIndex = 0  # explicitly select first filter
    if directory:
        dialog.Directory = System.Uri(directory)

    if dialog.ShowDialog(ui.RhinoEtoApp.MainWindow) == forms.DialogResult.Ok:
        selected_files = dialog.Filenames
        # Process the selected files
        for file_path in selected_files:
            print(f"Loading File: {file_path}")
        return file_path
    else:
        raise Exception("ERROR: Invalid file, or no file was selected")