# Autosave - Render: Automatically save .blend, .png and readme.txt files when rendering

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

The user interface appears in the Properties Area -> Output Properties -> Autosave on Render:

<img src="https://raw.githubusercontent.com/ICarryTheDustOfAJourney/Autosave-Render/assets/ui.png" alt="UI" style="width:16em; margin:2em" width="100"/>

- set the "Autosave on Render" checkmark to save the .blend file before rendering

- define/create the base-directory that will contain the new subdirectories

- optionally save a .png file after rendering

- optionally create a readme.txt. It can be previewed using the OS' file browser, its keywords will be indexed by the OS' search function.
    
    The content of readme.txt looks like:

      ---- Blender Generated Readme 211007_200350 myproject.blend
      -- Scene Infos:
           Blender V: 2.93.4
               Built: 2021-08-31 23:48:04
          Scene Name: Assets               
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

   The first section contains general infos about the Blender version and parameters used.
   
   The 2nd section contains the metadata note entered under Output Properties -> Metadata, if any.
   
   The 3rd section is the content of a document named "readme" from Blender's built-in texteditor, if a text with this name exists. It can contain information concerning this project, its history, keywords etc.

- optionally enter a short note to be appended to the new directory's name. Free shorthand reminder like "eevee only", "applied" or "!" when used in production etc. Use only characters allowed in your filesystem (Windows: no ":&lt;&gt;" etc). 

  This leads to folder names like "211007-145010-with geometry nodes, final version", intended as a quick reminder when revisiting the folder after a while

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

Optionally rename the parent folder with a speaking name for better orientation when browsing the filesystem later on. The latest and/or best version should then be in the latest & deepest leaf folder.

...unless you give up an idea too soon.

Enjoy!

---
