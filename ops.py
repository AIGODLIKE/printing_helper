from decimal import Decimal

import bpy

from .preset import preset_items_value, preset_items


class SwitchXY(bpy.types.Operator):
    bl_idname = "render.switch_xy"
    bl_label = "Switch XY"
    bl_description = "Switch Width Height"

    def execute(self, context):
        scene = context.scene
        ph = scene.printing_helper
        ph.physical_x, ph.physical_y = ph.physical_y, ph.physical_x
        return {"FINISHED"}


class PresetPPMValue(bpy.types.Operator):
    bl_idname = "render.preset_ppm_value"
    bl_label = "PresetPPMValue"

    value: bpy.props.IntProperty()

    def execute(self, context):
        from .update import update_ppm_factor
        bpy.ops.wm.context_set_float(data_path="scene.render.ppm_factor", value=self.value)
        update_ppm_factor()
        return {"FINISHED"}


class CreatePanel(bpy.types.Operator):
    bl_idname = "printing_helper.create_panel"
    bl_label = "Create Panel"
    bl_description = "Ctrl: Enter dimensions manually"

    width: bpy.props.FloatProperty(name="Width (CM)", default=21.0)
    height: bpy.props.FloatProperty(name="Height (CM)", default=29.7)
    name: bpy.props.StringProperty(default="Panel")

    ctrl: bpy.props.BoolProperty()

    def draw(self, context):
        layout = self.layout
        # layout.label(text=f"{self.ctrl}")
        layout.prop(self, "name")
        layout.prop(self, "width")
        layout.prop(self, "height")

    def invoke(self, context, event):
        wm = context.window_manager
        if event.ctrl:
            return wm.invoke_props_dialog(**{'operator': self})
        else:
            ph = context.scene.printing_helper
            self.width, self.height = ph.physical_y, ph.physical_x
            text = Preset.get_text(context)
            self.name = text if text != "Preset" else "Panel"
            return self.execute(context)

    def execute(self, context):
        from .utils import create_plane_by_bmesh
        create_plane_by_bmesh(self.width, self.height, self.name)
        return {"FINISHED"}


class Preset(bpy.types.Operator):
    bl_idname = "render.set_preset"
    bl_label = "Preset"

    preset: bpy.props.EnumProperty(items=preset_items)

    def execute(self, context):
        scene = context.scene
        ph = scene.printing_helper

        name, x, y = self.preset.split("_")
        ph.physical_x, ph.physical_y = Decimal(x), Decimal(y)
        return {"FINISHED"}

    @classmethod
    def get_text(cls, context) -> str:
        ph = context.scene.printing_helper
        min_value, max_value = min(ph.physical_x, ph.physical_y), max(ph.physical_x, ph.physical_y)
        key = str(round(min_value, 2)), str(round(max_value, 2))
        if i_name := preset_items_value.get(key):
            return i_name
        return "Preset"


def register():
    bpy.utils.register_class(SwitchXY)
    bpy.utils.register_class(PresetPPMValue)
    bpy.utils.register_class(Preset)
    bpy.utils.register_class(CreatePanel)


def unregister():
    bpy.utils.unregister_class(SwitchXY)
    bpy.utils.unregister_class(PresetPPMValue)
    bpy.utils.unregister_class(Preset)
    bpy.utils.unregister_class(CreatePanel)
