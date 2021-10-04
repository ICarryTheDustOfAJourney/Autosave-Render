bl_info = {
    "name": "Autosave-Render",
    "author": "Volker",
    "version": (1, 0, 1),
    "blender": (2, 92, 0),
    "location": "Properties Area > Output Properties > Autosave",
    "description": "Creates a YYMMDD-HHMMSS named subdirectory to save the .blend-file prior to rendering"
        "and a .png file after rendering. UI resides in the Output Properties."
        "Manually delete superflous sub-directories by <Shift>-Clicking on the folder icon in Blender"
        "to open the base folder in your OS filebrowser.",
    "warning": "",
    "wiki_url": "",
    "category": "Render"}

import bpy
import os
import datetime
from pathlib import Path
from bpy.app.handlers import persistent

#set destination dir default
base_path = ''

@persistent
# save .blend in a newly created subdirectory named yymmdd-hhmmss
def autosave_blend_before_render(self):

    # generate destination dir name

    #default = output path
    path = bpy.context.scene.render.filepath 
    
    # own path found -> use it
    if bpy.context.scene.autosave_render_settings.autosave_directory:
        path = bpy.context.scene.autosave_render_settings.autosave_directory 

    # set the global autosave path for the image after rendering       
    global base_path
    
    # add timestamp
    now = datetime.datetime.now()
    base_path = os.path.join(path, now.strftime('%y%m%d_%H%M%S'))

    # not checkmarked -> do nothing
    if not bpy.context.scene.autosave_render_settings.use_autosave_render:
        return

    # dir ! existing -> create
    if not os.path.exists(base_path):
        os.makedirs(base_path)    

    # append filename to path
    filename = os.path.basename(bpy.data.filepath)
    
    # no filename -> invent one
    if not filename:
        filename = "default.blend"
        
    filepath = os.path.join(base_path, filename)

    # save current .blend file as a copy
    bpy.ops.wm.save_as_mainfile(filepath= filepath, copy=True) 

    if not bpy.context.scene.autosave_render_settings.use_autosave_bitmap:
        base_path = ""
      
@persistent        
# save .png in a newly created subdirectory named yymmdd-hhmmss
def autosave_bitmap_after_render(self):

    # not checkmarked -> do nothing
    if not bpy.context.scene.autosave_render_settings.use_autosave_bitmap:
        return

    global base_path

    # append filename to path
    filename = os.path.basename(bpy.data.filepath)
    
    # no filename -> invent one
    if not filename:
        filename = "default.blend"
    
    # append filename to path created before rendering
    filepath = os.path.join(base_path, filename + ".png")
    
    # save current rendering
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.data.images["Render Result"].save_render(filepath)    

    # reset path for next try
    base_path = ""

# setter & getter for base-directory property
def set_directory(self, value):
    path = Path(value)
    if path.is_dir():
        self["autosave_directory"] = value

def get_directory(self):
    return self.get("autosave_directory", bpy.context.scene.render.filepath )

# properties definition        
class AutoFilepathSettings(bpy.types.PropertyGroup):
    
    use_autosave_render: bpy.props.BoolProperty(name="Autosave",
                                              description="Automatic save .blend prior to rendering in a timestamped sub-directory",
                                              default=False)

    use_autosave_bitmap: bpy.props.BoolProperty(name="Autosave .png after render",
                                              description="Automatic save bitmap file AFTER rendering in a timestamped sub-directory",
                                              default=False)
                                              
    autosave_directory: bpy.props.StringProperty(name="Directory",
                                        description="Directory for the timestamped subdirectories",
                                        default="/",
                                        maxlen=4096,
                                        subtype="DIR_PATH",
                                        set=set_directory,
                                        get=get_directory)                                              

# panel class
class AUTOFILEPATH_PT_panel(bpy.types.Panel):
    
    bl_label = "Autosave"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.prop(context.scene.autosave_render_settings, "use_autosave_render", text="")

    def draw(self, context):
        layout = self.layout
        #layout.use_property_split = True

        row = layout.row()
        row.label(text="Base Directory:")
        
        row = layout.row()
        row.prop(context.scene.autosave_render_settings, "autosave_directory", text="")
        
        row = layout.row( )
        row.prop(context.scene.autosave_render_settings, "use_autosave_bitmap")

# group all classes togeter
classes = (AutoFilepathSettings, AUTOFILEPATH_PT_panel)

# install
def register():
    
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.autosave_render_settings = bpy.props.PointerProperty(type=AutoFilepathSettings)
    
    # establish callbacks
    if autosave_blend_before_render not in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.append(autosave_blend_before_render)

    if autosave_bitmap_after_render not in bpy.app.handlers.render_post:
        bpy.app.handlers.render_post.append(autosave_bitmap_after_render)

# un-install
def unregister():
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.autosave_render_settings

    # un-establish callbacks
    if autosave_blend_before_render in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.remove(autosave_blend_before_render)
        
    if autosave_bitmap_after_render in bpy.app.handlers.render_post:
        bpy.app.handlers.render_pre.remove(autosave_bitmap_after_render)

if __name__ == "__main__":
    register()
