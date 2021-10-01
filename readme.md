# Autosave - Automatically save .blend and .png files when rendering images

## Purpose 

Usually, creating images/animations with Blender is a highly iterative trial-and-error process, that can lead into dead ends when using wrong techniques or taking bad artistic choices.
When trying to resume at a better, former version, it can be difficult to find the matching .blend file for that state.

When activated, every &lt;F12> will save the .blend-file of that moment in a unique, dynamically created directory, optionally together with the render image in a separate .png file after the rendering finished. 

This add-on creates new sub-directories named YYMMDD-hhmmss in a base-directroy of your choice. YYMMDD-hhmmss is the timestamp when the renderprocess was started.

It provides an easy way to document progress over time and to jump back to an old state, if required.

Might be understood as a basic source control system for the ~~poor~~ artists.

## Installation

- [download](https://github.com/ICarryTheDustOfAJourney/Autosave-Render/raw/main/autosave.py) the .py file to a location of your choice
- in Blender: Edit -> Preferences-> Add-on -> Install... and pick the .py file
- don't forget to activate it 

Developed & tested under Windows 10 on Blender V2.92.0 and 3.0 Alpha.
Should work on other OSes and/or in older Blender versions too.

## Usage

The user interface appears in the Properties Area -> Output Properties -> Autosave. 

- create/define the base-directory that will contain the dynamically created subdirectories
- enable the "Autosave" checkmark to save .blend files before rendering
- enable "Autosave .png after render" to save a .png file of the render image after rendering
- render (&lt;F12>)

### Hints
- the dimensions of the .png file are determined by the output properties
- this add-on doesn't affect other settings like output paths etc
- it doesn't make much sense when active while creating animations (&lt;Ctrl>-&lt;F12>)
- manually delete superflous directories
- &lt;Shift>-Click on the folder icon opens the base-directory in your OS' file system browser

## Advanced usage

Shift your base-directory into the new sub-directory once you think you achieved significant progress with that render.
This transforms the otherwise linear folder structure into a tree-structure, having elaborated versions in its branches.

Optionally rename the parent folder with a speaking name for better orientation lateron. The latest and/or best version should then be in the latest & deepest leaf folder.

...unless you give up an idea too soon.

---
