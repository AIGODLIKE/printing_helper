import bpy


class SwitchXY(bpy.types.Operator):
    bl_idname = "render.switch_xy"
    bl_label = "Switch XY"

    def execute(self, context):
        scene = context.scene
        ph = scene.printing_helper
        ph.physical_x, ph.physical_y = ph.physical_y, ph.physical_x
        return {"FINISHED"}


class PresetItem(bpy.types.Operator):
    bl_idname = "render.preset_item"
    bl_label = "Preset Item"

    preset: bpy.props.EnumProperty(
        items=(
            ("custom_1_1", "Custom", ""),
            ("A0_84.1_118.9", "A0 (84.1x118.9 cm)", ""),
            ("A1_59.4_84.1", "A1 (59.4x84.1 cm)", ""),
            ("A2_42.0_59.4", "A2 (42.0x59.4 cm)", ""),
            ("A3_29.7_42.0", "A3 (29.7 42.0 cm)", ""),
            ("A4_21.0_29.7", "A4 (21.0x29.7 cm)", ""),
            ("A5_14.8_21.0", "A5 (14.8x21.0 cm)", ""),
            ("A6_10.5_14.8", "A6 (10.5x14.8 cm)", ""),
            ("A7_7.4_10.5", "A7 (7.4x10.5 cm)", ""),
            ("A8_5.2_7.4", "A8 (5.2x7.4 cm)", ""),
            ("A9_3.7_5.2", "A9 (3.7x5.2 cm)", ""),
            ("A10_2.6_3.7", "A10 (2.6x3.7 cm)", ""),

            ("B0_100.0_141.4", "B0 (100.0x141.4 cm)", ""),
            ("B1_70.7_100.0", "B1 (70.7x100.0 cm)", ""),
            ("B2_50.0_70.7", "B2 (50.0x70.7 cm)", ""),
            ("B3_35.3_50.0", "B3 (35.3x50.0 cm)", ""),
            ("B4_25.0_35.3", "B4 (25.0x35.3 cm)", ""),
            ("B5_17.6_25.0", "B5 (17.6x25.0 cm)", ""),
            ("B6_12.5_17.6", "B6 (12.5x17.6 cm)", ""),
            ("B7_8.8_12.5", "B7 (8.8x12.5 cm)", ""),
            ("B8_6.2_8.8", "B8 (6.2x8.8 cm)", ""),
            ("B9_4.4_6.2", "B9 (4.4x6.2 cm)", ""),
            ("B10_3.1_4.4", "B10 (3.1x4.4 cm)", ""),

            ("C0_91.7_129.7", "C0 (91.7x129.7 cm)", ""),
            ("C1_64.8_91.7", "C1 (64.8x91.7 cm)", ""),
            ("C2_45.8_64.8", "C2 (45.8x64.8 cm)", ""),
            ("C3_32.4_45.8", "C3 (32.4x45.8 cm)", ""),
            ("C4_22.9_32.4", "C4 (22.9x32.4 cm)", ""),
            ("C5_16.2_22.9", "C5 (16.2x22.9 cm)", ""),
            ("C6_11.4_16.2", "C6 (11.4x16.2 cm)", ""),
            ("C7_8.1_11.4", "C7 (8.1x11.4 cm)", ""),
            ("C8_5.7_8.1", "C8 (5.7x8.1 cm)", ""),
            ("C9_4.0_5.7", "C9 (4.0x5.7 cm)", ""),
            ("C10_2.8_4.0", "C10 (2.8x4.0 cm)", ""),

            ("Letter_21.6_27.9", "Letter (21.6x27.9 cm)", ""),
            ("Legal_21.6_35.6", "Legal (21.6x35.6 cm)", ""),
            ("Legal junior_20.3_12.7", "Legal junior (20.3x12.7 cm)", ""),
            ("Ledger_43.2_27.9", "Ledger (43.2x27.9 cm)", ""),
            ("Tabloid_27.9_43.2", "Tabloid (27.9x43.2 cm)", ""),

            ("ANSI C_43.2_55.9", "ANSI C (43.2x55.9 cm)", ""),
            ("ANSI D_55.9_86.4", "ANSI D (55.9x86.4 cm)", ""),
            ("ANSI E_86.4_111.8", "ANSI E (86.4x111.8 cm)", ""),

            ("Arch A_22.9_30.5", "Arch A (22.9x30.5 cm)", ""),
            ("Arch B_30.5_45.7", "Arch B (30.5x45.7 cm)", ""),
            ("Arch C_45.7_61.0", "Arch C (45.7x61.0 cm)", ""),
            ("Arch D_61.0_91.4", "Arch D (61.0x91.4 cm)", ""),
            ("Arch E_91.4_121.9", "Arch E (91.4x121.9 cm)", ""),
            ("Arch E1_76.2_106.7", "Arch E1 (76.2x106.7 cm)", ""),
            ("Arch E2_66.0_96.5", "Arch E2 (66.0x96.5 cm)", ""),
            ("Arch E3_68.6_99.1", "Arch E3 (68.6x99.1 cm)", ""),
        )
    )
    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        scene = context.scene
        return {"FINISHED"}


def register():
    bpy.utils.register_class(SwitchXY)
    bpy.utils.register_class(PresetItem)


def unregister():
    bpy.utils.unregister_class(SwitchXY)
    bpy.utils.unregister_class(PresetItem)
