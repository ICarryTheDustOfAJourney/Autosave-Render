# Autosave - Automatically save .blend and .png files when rendering images

## Purpose 

This add-on provides an easy way to document & preserve a project's progress over time and to jump back to an arbitrary previous state, if required.

It saves the .blend, .png (render image, optional) and a readme.txt (optional infos) -file in a new, dedicated subdirectory on every rendering. 

The new sub-directories are named YYMMDD-hhmmss + an optional short note, located in a base-directory of your choice.

Creating images/animations with Blender is usually a highly iterative trial-and-error process, that can lead into dead ends when using wrong techniques or taking bad artistic choices.

When trying to resume at a former version, it can be difficult to find the matching .blend file for that state of the project.

This add-on can be understood as a basic but efficient source control system for the ~~poor~~ artist.

## Installation

- [download](https://github.com/ICarryTheDustOfAJourney/Autosave-Render/raw/main/autosave.py) the .py file to a location of your choice
- in Blender: Edit -> Preferences-> Add-on -> Install... and pick the .py file
- don't forget to activate it by setting the checkmark

Developed & tested under Windows 10 on Blender V2.90.1, 2.93 and 3.0 Alpha.
It should work on other OSes and/or in older Blender versions too.

## Usage

The user interface appears in the Properties Area -> Output Properties -> Autosave:
<img src="data:image/png;base64,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" alt="UI" style="width:20em; margin:2em" width="100"/>

- set the "Autosave on Render" checkmark to save .blend files before rendering

- define/create the base-directory that will contain the new subdirectories

- optionally save a .png file after rendering

- optionally create a readme.txt. It can be previewed using the OS' file browser, its keywords will be indexed by the OS' search function.
    
    The content:

      ---- Blender Generated Readme 211007_200350 myproject.blend
      -- Scene Infos:
           Blender V: 2.93.4
               Built: 2021-08-31 23:48:04
       Current Frame: 1
        Resolution %: 100
      View Transform: Filmic
                Look: None
            Exposure: 0.0
               Gamma: 1.0
              Engine: CYCLES
               Samples: 128
           Feature Set: EXPERIMENTAL
                Device: CPU
      -- Metadata Note:
       note from the output properties
      -- Readme Text:
      This is a text from the readme text. 
      It can contain a history of the project or longer annotations.
      ---

   The first section contains common infos about the Blender version and paramters used.
   
   The 2nd section contains the metadata note entered under Output Properties -> Metadata, if any.
   
   The 3rd section is the content of a document named "readme" from Blender's built-in texteditor, if a text with this name exists. It can contain information concerning this project, its history, keywords etc.

- optionally enter a short note to be appended to the new directory's name. Free shorthand reminder like "evee only", "applied" or "!" when used in production etc. Use only characters allowed in your filesystem (Windows: no ":&lt;&gt;" etc). 

  This leads to folder names like "211007-145010-with geometry nodes, final version", intended as a quick hint when revisiting the folder after a while

- finally start the renderprocess hitting &lt;F12> and browse the new subdirectory

### Hints
- the dimensions of the .png file are determined by the output properties
- this add-on doesn't affect other settings like output paths etc
- it doesn't make much sense when active while creating animations (&lt;Ctrl>-&lt;F12>)
- manually delete directories if they are not needed
- &lt;Shift>-Click on the folder icon opens the base-directory in your OS' file system browser
- because the .blend file is saved before and the .png file after rendering, rendertime is documented too
- choose your base-directory on an external or network drive. This may save your live if your SSD dies

## Advanced usage

Shift your base-directory into the new sub-directory once you think you achieved significant progress with that render.
This transforms the otherwise linear folder structure into a tree, having elaborated versions in its branches.

Optionally rename the parent folder with a speaking name for better orientation when browsing the filesystem lateron. The latest and/or best version should then be in the latest & deepest leaf folder.

...unless you give up an idea too soon.

Enjoy!

---
