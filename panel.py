import bpy

from .ops import SwitchXY, Preset


# NOTE: `as_float_32` is needed because Blender stores this value as a 32bit float.
# Which won't match Python's 64bit float.
def as_float_32(f):
    from struct import pack, unpack
    return unpack("f", pack("f", f))[0]


class PRINTINGHELPER_PT_panel(bpy.types.Panel):
    bl_label = "Printing  Helper"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    bl_parent_id = "RENDER_PT_format"

    def draw_header_preset(self, context):
        row = self.layout.row(align=True)
        row.operator(SwitchXY.bl_idname, text="", icon="UV_SYNC_SELECT")
        row.operator_menu_enum(Preset.bl_idname, text=Preset.get_text(context), property="preset")

    def draw(self, context):
        from bpy.types import RENDER_PT_output_pixel_density
        from .ops import PresetPPMValue

        scene = context.scene
        ph = scene.printing_helper
        render = scene.render

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        column = layout.column(align=True)

        if render.ppm_base != as_float_32(0.0254):  # 不是英尺dpi单位
            ops = column.operator("wm.context_set_float", text="Reset as Inch")
            ops.data_path = "scene.render.ppm_base"
            ops.value = 0.0254
            col = column.column(align=True)
            col.label(
                text="The PPM base unit is not set to inches, the output DPI parameter will not match the actual parameter!")
            col.label(text="Must be reset to inches!")
        else:
            column.prop(ph, "physical_x")
            column.prop(ph, "physical_y")

            column.separator()
            column.prop(render, "ppm_factor", text="DPI")

            sp = column.split(factor=0.4, align=True)
            sp.alignment = "RIGHT"
            sp.label(text="Preset")
            row = sp.row(align=True)
            for i in (72, 150, 300):
                ops = row.operator(PresetPPMValue.bl_idname, text=str(i))
                ops.value = i

            column.separator()
            column.row(align=True).prop(ph, "mode", expand=True)


def register():
    bpy.utils.register_class(PRINTINGHELPER_PT_panel)


def unregister():
    bpy.utils.unregister_class(PRINTINGHELPER_PT_panel)
