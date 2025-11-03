import bpy
from bl_operators.presets import AddPresetBase
from bl_ui.utils import PresetPanel


class RENDER_PT_printing_helper_presets(PresetPanel, bpy.types.Panel):
    bl_label = "Printing Helper Presets"
    preset_subdir = "printing"
    preset_operator = "script.execute_preset"
    preset_add_operator = "render.printing_preset_add"


class AddPresetPrinting(AddPresetBase, bpy.types.Operator):
    """Add or remove a Printing Preset"""
    bl_idname = "render.printing_preset_add"
    bl_label = "Add Printing Preset"
    preset_menu = "RENDER_PT_printing_helper_presets"

    preset_defines = [
        "render = bpy.context.scene.render",
        "printing = bpy.context.scene.printing_helper"
    ]

    preset_values = [
        "render.ppm_factor",
        "render.ppm_base",
    ]

    preset_subdir = "render"


def register():
    bpy.utils.register_class(RENDER_PT_printing_helper_presets)


def unregister():
    bpy.utils.unregister_class(RENDER_PT_printing_helper_presets)
