import bpy


class PRINTINGHELPER_PT_panel(bpy.types.Panel):
    bl_label = "Pringing Helper"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    bl_parent_id = "RENDER_PT_format"

    def draw_header_preset(self, _context):
        from .preset import RENDER_PT_printing_helper_presets
        RENDER_PT_printing_helper_presets.draw_panel_header(self.layout)

    def draw(self, context):
        from bpy.types import RENDER_PT_output_pixel_density

        scene = context.scene
        ph = scene.printing_helper
        render = scene.render

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        column = layout.column(align=True)

        def as_float_32(f):
            from struct import pack, unpack
            return unpack("f", pack("f", f))[0]

        if render.ppm_base != as_float_32(0.0254):  # 不是英尺dpi单位
            ops = column.operator("wm.context_set_float", text="Reset as Inch")
            ops.data_path = "scene.render.ppm_base"
            ops.value = 0.0254
            col = column.column(align=True)
            col.label(text="PPM 基数未设置为英寸单位,输出DPI参数将与实际参数不一至!")
            col.label(text="需重置为英寸单位")
        else:
            column.row(align=True).prop(ph, "mode", expand=True)
            column.prop(render, "ppm_factor", text="DPI")
            column.prop(ph, "physical_width")
            column.prop(ph, "physical_height")
        return

        self.draw_dpi(column, context)
        self.draw_pixeldensity(column, render)

        # NOTE: `as_float_32` is needed because Blender stores this value as a 32bit float.
        # Which won't match Python's 64bit float.

        column.separator()
        text = bpy.app.translations.pgettext_iface(unit_name)
        th = bpy.app.translations.pgettext_iface("Physical Height")
        tw = bpy.app.translations.pgettext_iface("Physical Width")

        column.prop(render, "ppm_base", text="Base")


def register():
    bpy.utils.register_class(PRINTINGHELPER_PT_panel)


def unregister():
    bpy.utils.unregister_class(PRINTINGHELPER_PT_panel)
