# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import datetime
import os
from pathlib import Path

import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Autosave-Render",
    "author": "icarrythedustofajourney (Volker)",
    "version": (1, 2, 6),
    "blender": (2, 90, 1),
    "location": "Properties Area > Output Properties > Autosave",
    "description": "Creates a YYMMDD-HHMMSS named subdirectory to save the .blend-file prior to rendering"
    "and a .png file after rendering. UI resides in the Output Properties."
    "Enter short notes to be appended as reminders to the subdirectory's name."
    "Manually delete superflous sub-directories by <Shift>-Clicking on the folder icon in Blender"
    "to open the base folder in your OS filebrowser.",
    "warning": "",
    "wiki_url": "https://github.com/ICarryTheDustOfAJourney/Autosave-Render",
    "category": "Render"
}

# ------------------
# event-handlers:
# ------------------


@persistent
def autosave_blend_before_render(scene):
    # save .blend in a newly created subdirectory named yymmdd-hhmmss

    # default = output path
    path = scene.render.filepath

    # own path found -> use it
    if scene.autosave_render_settings.autosave_directory:
        path = scene.autosave_render_settings.autosave_directory

    # set the global autosave path for the image after rendering
    global base_path

    # add timestamp
    now = datetime.datetime.now()
    base_path = os.path.join(path, now.strftime('%y%m%d_%H%M%S'))

    # not checkmarked -> do nothing
    if not scene.autosave_render_settings.use_autosave_render:
        return

    # note entered -> append to the new dirname
    if scene.autosave_render_settings.use_autosave_note:
        base_path += "-" + scene.autosave_render_settings.use_autosave_note

    # dir ! existing -> create
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # append filename to path
    filename = os.path.basename(bpy.data.filepath)

    # no filename -> invent one
    if not filename:
        filename = "untitled.blend"

    filepath = os.path.join(base_path, filename)

    # save current .blend file as a copy
    bpy.ops.wm.save_as_mainfile(filepath=filepath, copy=True)

    # text named readme found -> export it into readme.txt
    if scene.autosave_render_settings.use_autosave_readme:

        # start with datetime
        text = "---- Blender Generated Readme " + \
            now.strftime('%y%m%d_%H%M%S') + " " + filename

        # append scene infos
        text += "\n\n-- Scene Infos:" + scene_infos(scene)

        # metadata note set -> append
        if scene.render.stamp_note_text:
            text += "\n\n-- Metadata Note:\n" + scene.render.stamp_note_text

        # readme text found -> append
        if "readme" in bpy.data.texts:
            text += "\n\n-- Readme Text:\n" + \
                bpy.data.texts['readme'].as_string()

        # append EOF marker
        text += "\n\n---"

        # build readme file path/name
        path = Path(os.path.join(base_path, "readme.txt"))

        # write text to file
        path.write_text(text)

    if not scene.autosave_render_settings.use_autosave_png:
        base_path = ""


@persistent
def autosave_bitmap_after_render(scene):
    # save .png in a newly created subdirectory named yymmdd-hhmmss

    # not checkmarked -> do nothing
    if not scene.autosave_render_settings.use_autosave_png:
        return

    if not scene.autosave_render_settings.use_autosave_render:
        return

    # append .blend filename to path
    filename = os.path.basename(bpy.data.filepath)

    # no filename -> invent one
    if not filename:
        filename = "default.blend"

    global base_path

    # append filename to path created before rendering
    filepath = os.path.join(base_path, filename + ".png")

    # save current rendering
    scene.render.image_settings.file_format = 'PNG'
    bpy.data.images["Render Result"].save_render(filepath)

    # reset path for next try
    base_path = ""

# ------------------
# utilities:
# ------------------


# set destination dir default
base_path = ""


def scene_infos(scene):
    # return common scene infos as text

    # get shortcuts
    view_settings = scene.view_settings

    # build readme text
    note = "\n     Blender V: " + str(bpy.app.version_string)
    note += "\n         Built: " + \
        bpy.app.build_date.decode("utf-8") + " " + \
        bpy.app.build_time.decode("utf-8")
    #note += "\n  Version File: " + str(bpy.app.version_file)
    #note += "\n  Version Data: " + str(bpy.data.version)
    note += "\n    Scene Name: " + str(scene.name)
    note += "\n Current Frame: " + str(scene.frame_current)
    note += "\n  Resolution %: " + str(scene.render.resolution_percentage)
    note += "\nView Transform: " + str(view_settings.view_transform)
    note += "\n          Look: " + str(view_settings.look)
    note += "\n      Exposure: " + str(view_settings.exposure)
    note += "\n         Gamma: " + str(view_settings.gamma)
    note += "\n        Engine: " + str(scene.render.engine)

    if str(scene.render.engine) == 'CYCLES':

        cycles = scene.cycles
        note += "\n             Samples: " + str(cycles.samples)
        note += "\n         Feature Set: " + str(cycles.feature_set)
        note += "\n              Device: " + str(scene.cycles.device)

        if cycles.use_denoising:
            note += "\n            Denoiser: " + str(cycles.denoiser)

    if str(scene.render.engine) == 'BLENDER_EEVEE':

        eevee = scene.eevee
        note += "\n             Samples: " + str(eevee.taa_render_samples)

    return note


# glob var holding the message
msg_text = ""


def show_msg(self, context):

    # show msg to user as popup
    global msg_text
    self.layout.label(text=msg_text)

# ------------------
# setters & getters:
# ------------------


def set_directory(self, value):

    path = Path(value)
    if path.is_dir():
        self["autosave_directory"] = value


def get_directory(self):

    return self.get("autosave_directory", bpy.context.scene.render.filepath)


def set_note(self, value):

    # avoid leading, trailing whitespaces leading to invalid paths
    value = value.strip()

    # no note -> save & quit
    if(value == ""):
        self["use_autosave_note"] = value
        return

    # check for valid pathname, eg ':>' etc arent allowed chars in windows
    # test-create a folder having that name
    testpath = os.path.join(self["autosave_directory"], value)

    try:
        os.makedirs(testpath)
        # came to here = success
        self["use_autosave_note"] = value
        # delete testfolder
        os.removedirs(testpath)

    except:
        # inform user
        global msg_text
        msg_text = value
        bpy.context.window_manager.popup_menu(
            show_msg, title="Note contains invalid characters", icon='ERROR')


def get_note(self):

    # return prop when existing
    try:
        return self["use_autosave_note"]

    except:
        return ""


# ------------------
# properties definition:
# ------------------


class AutoFilepathSettings(bpy.types.PropertyGroup):

    use_autosave_render: bpy.props.BoolProperty(name="Autosave on Render",
                                                description="Automatic save .blend before rendering",
                                                default=False)

    use_autosave_png: bpy.props.BoolProperty(name="Save .png after render",
                                             description="Automatic save render image after rendering",
                                             default=False)

    autosave_directory: bpy.props.StringProperty(name="Directory",
                                                 description="Base-directory for the timestamped subdirectories to be created before rendering",
                                                 default="/",
                                                 maxlen=4096,
                                                 subtype="DIR_PATH",
                                                 set=set_directory,
                                                 get=get_directory)

    use_autosave_note: bpy.props.StringProperty(name="Note",
                                                description="Optional short note, appended to the name of the new subdirectory. Don't use characters forbidden in filenames (':' etc)",
                                                default="",
                                                maxlen=200,
                                                set=set_note,
                                                get=get_note)

    use_autosave_readme: bpy.props.BoolProperty(name="Save readme",
                                                description="Export readme text into separate readme.txt, to be indexed by your OS",
                                                default=False)


class AUTOFILEPATH_PT_panel(bpy.types.Panel):
    # UI panel class

    bl_label = "Autosave on Render"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.prop(context.scene.autosave_render_settings,
                         "use_autosave_render", text="")

    def draw(self, context):

        layout = self.layout
        enabled = context.scene.autosave_render_settings.use_autosave_render

        # layout.use_property_split = True
        row = layout.row()
        row.label(text="Base Directory:")
        row.enabled = enabled

        row = layout.row()
        row.prop(context.scene.autosave_render_settings,
                 "autosave_directory", text="")
        row.enabled = enabled

        row = layout.row()
        row.prop(context.scene.autosave_render_settings, "use_autosave_png")
        row.enabled = enabled

        row = layout.row()
        row.prop(context.scene.autosave_render_settings,
                 "use_autosave_readme")
        row.enabled = enabled

        row = layout.row()
        row.label(text="Note:")
        row.enabled = enabled

        row = layout.row()
        row.prop(context.scene.autosave_render_settings,
                 "use_autosave_note", text="")
        row.enabled = enabled


# group all classes togeter
classes = (AutoFilepathSettings, AUTOFILEPATH_PT_panel)

# ------------------
# installation in blender:
# ------------------


def register():
    # establish stuff

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.autosave_render_settings = bpy.props.PointerProperty(
        type=AutoFilepathSettings)

    # establish callbacks
    if autosave_blend_before_render not in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.append(autosave_blend_before_render)

    if autosave_bitmap_after_render not in bpy.app.handlers.render_post:
        bpy.app.handlers.render_post.append(autosave_bitmap_after_render)


def unregister():
    # un-install
    # called when add-on is disabled

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.autosave_render_settings

    # un-establish callbacks
    if autosave_blend_before_render in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.remove(autosave_blend_before_render)

    if autosave_bitmap_after_render in bpy.app.handlers.render_post:
        bpy.app.handlers.render_post.remove(autosave_bitmap_after_render)


# make add-on runnable as script too
if __name__ == "__main__":
    register()
