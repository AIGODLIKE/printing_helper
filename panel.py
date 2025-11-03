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
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene
        rd = scene.render

        bpy.types.RENDER_PT_output_pixel_density.draw_pixeldensity(layout, rd)


def register():
    bpy.utils.register_class(PRINTINGHELPER_PT_panel)


def unregister():
    bpy.utils.unregister_class(PRINTINGHELPER_PT_panel)
