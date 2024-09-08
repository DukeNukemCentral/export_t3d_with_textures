# export_t3d_with_textures
takes blender objects and exports T3D data to clipboard. for use with Duke Nukem Forever.

## Blender Object to Unreal T3D Plug-in With texture support for DNF01/DNF2011  
by Snake Plissken and ZNukem

### DESCRIPTION

This plugin for Blender allows conversion of Duke Nukem Zero Hour Maps, and DN3D Maps into Unreal T3D format, specifically tailored for use with DNF01 and DNF2011. The plugin automates the renaming of materials and generates T3D data, which can be directly copied to the clipboard.

NOTE: You may need blender 4.0 or higher. You will need to have imported a build map or Zero Hour Assets map from https://drive.google.com/file/d/1GHzc_voPoh2MaWEADwUrzBEUtSutbLdY/view?usp=sharing with the following plugin:
https://github.com/jensnt/io_import_build_map
if you intend on using a Zero Hour map you must first make sure that the the build import add-on's options have the valid texture path specifed.
 the Art folder located in the Tiles folder. " Zero Hour Resources\Tiles\art " 

### FEATURES

- **Update Material Names:** Strips the "picnum" prefix from material names.
- **Update DN3D object material names**  modifies the names of materials in Blender to match a specific format required for Duke Nukem 3D (DN3D) imported objects. It renames any material starting with "picnum" to follow a XXXX_XXX format. This is particularly useful for ensuring that material names comply with expected naming conventions for further processing or and importing with texture support into DNF 01 or 11
- **Copy T3D to Clipboard:** Converts the selected Blender object to T3D format and copies the data to the clipboard.

### INSTALLATION

#### Simple Installation

1. Download `dnzh_t3d_plugin.zip`.
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click `Install`, select `dnzh_t3d_plugin.zip`, and enable the plugin.

#### Manual Installation
If other way don't work, then use this to add it in manually.

1. Locate your Blender installation directory and navigate to `blender/scripts/addons/`.
2. Copy the `ZH-TO-T3D` folder into this `addons` directory.
3. Open Blender and go to `Edit > Preferences > Add-ons`.
4. Find and enable the `DN Zero Hour To T3D Plugin`.

### USAGE

1. In Blender, select the object you want to export.
2. Open the `T3D` tab from the 3D View sidebar.
3. Click `Update Material Names` to rename Zero Hour materials of maps imported from zero hour. If your working with a DUKE3D.GRP map from DN3D then use the Update DN3D object material names Button instead.  
4. Click `Copy T3D to Clipboard` to generate T3D data and copy it to the clipboard. Paste the data from the clipboard into a text document and then save it with a `.t3d` extension
5. Import Textures that are used on your blender object into DNF editor.
6. Import the file into Unreal Editor with Brush > Import.
7. Subtract Brush.
8. WHEN IN DUKE NUKEM FOREVER EDITOR: If faces are backwords in DNF editor make sure to go back to blender and wile in edit mode, flip
    all the objects face normals or all that are effected.
9. WILE STILL IN DUKE NUKEM FOREVER EDITOR and if textures appear to be contorted or stretched incorrectly, to fix this you may want to select all faces > surface properties > align > align by planer.

### SYSTEM REQUIREMENTS

- possibly Blender 4.00 or higher
- Python 3.7+

### LICENSE

This plugin is licensed under the MIT License.  
You can get a copy or revision of this license at:  
[https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)


