from decimal import Decimal

import bpy
import numpy as np
from bpy.app.translations import (
    pgettext_iface as iface_,
)


class PRINTINGHELPER_PT_panel(bpy.types.Panel):
    bl_label = "Pringing Helper"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    bl_parent_id = "RENDER_PT_format"

    @staticmethod
    def draw_pixeldensity(layout, rd):
        """
        scripts\startup\bl_ui\properties_output.py L432
        """
        from bpy.types import RENDER_PT_output_pixel_density
        if RENDER_PT_output_pixel_density._preset_class is None:
            RENDER_PT_output_pixel_density._preset_class = bpy.types.RENDER_MT_pixeldensity_presets

        args = rd.ppm_base, RENDER_PT_output_pixel_density._preset_class.bl_label
        pixeldensity_label_text, show_pixeldensity = RENDER_PT_output_pixel_density._draw_pixeldensity_label(*args)

        layout.prop(rd, "ppm_factor", text="Pixels")

        row = layout.split(factor=0.4, align=True)
        row.alignment = 'RIGHT'
        row.label(text="Unit")
        row.menu("RENDER_MT_pixeldensity_presets", text=pixeldensity_label_text)

        if show_pixeldensity:
            col = layout.column(align=True)
            col.prop(rd, "ppm_base", text="Base")

    def draw_header_preset(self, _context):
        from .preset import RENDER_PT_printing_helper_presets
        RENDER_PT_printing_helper_presets.draw_panel_header(self.layout)

    def draw_dpi(self, layout, context):
        """
        # xasp = Decimal(1.0)
        # yasp = Decimal(1.0)
        # if render.resolution_x < render.resolution_y:
        #     yasp = Decimal(render.resolution_x) / Decimal(render.resolution_y)
        # elif render.resolution_x > render.resolution_y:
        #     xasp = Decimal(render.resolution_y) / Decimal(render.resolution_x)
        :param layout:
        :param context:
        :return:
        """
        scene = context.scene
        render = scene.render

        ppm_base = render.ppm_base
        ppm_factor = render.ppm_factor
        total_ppm = np.multiply(ppm_base, ppm_factor)

        x = render.resolution_x / total_ppm
        y = render.resolution_y / total_ppm
        layout.label(text=f"w:{np.divide(0.0254, ppm_base)}")
        layout.label(text=f"s:{np.multiply(254, ppm_base)}")
        layout.label(text=f"total_ppm:{total_ppm}")
        layout.label(text=f"Resolution:{x} {y}")

    def draw(self, context):
        from bpy.types import RENDER_PT_output_pixel_density

        scene = context.scene
        render = scene.render

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        column = layout.column(align=True)

        self.draw_dpi(column, context)
        self.draw_pixeldensity(column, render)

        # NOTE: `as_float_32` is needed because Blender stores this value as a 32bit float.
        # Which won't match Python's 64bit float.
        def as_float_32(f):
            from struct import pack, unpack
            return unpack("f", pack("f", f))[0]

        unit_name = {
            as_float_32(0.0254): iface_("Inch"),
            as_float_32(0.01): iface_("Centimeter"),
            as_float_32(1.0): iface_("Meter"),
        }.get(render.ppm_base, "Custom")

        column.separator()
        text = bpy.app.translations.pgettext_iface(unit_name)
        th = bpy.app.translations.pgettext_iface("Physical Height")
        tw = bpy.app.translations.pgettext_iface("Physical Width")
        column.prop(scene.printing_helper, "physical_width", text=f"{tw}({text})")
        column.prop(scene.printing_helper, "physical_height", text=f"{th}({text})")

        column.prop(render, "ppm_base", text="Base")


def register():
    bpy.utils.register_class(PRINTINGHELPER_PT_panel)


def unregister():
    bpy.utils.unregister_class(PRINTINGHELPER_PT_panel)
