bl_info = {
    "name": "3D Printing Tools",
    "author": "Filipe Lopes",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > 3D Printing Tools",
    "description": "Utilities to prepare models for 3D printing",
    "category": "Object",
}

import bpy

from . import utils


class OBJECT_OT_remove_irregular_faces(bpy.types.Operator):
    bl_idname = "object.remove_irregular_faces"
    bl_label = "Remove irregular faces"
    bl_description = "Triangulate faces with more than four vertices on the selected mesh objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and any(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        result = utils.remove_irregular_faces(context)

        if result["processed_objects"] == 0:
            self.report({"WARNING"}, "Select at least one mesh object")
            return {"CANCELLED"}

        if result["corrected_faces"] == 0:
            self.report({"INFO"}, "No irregular faces found in the selected objects")
            return {"FINISHED"}

        self.report(
            {"INFO"},
            f"Corrected {result['corrected_faces']} irregular faces in {result['processed_objects']} object(s)",
        )
        return {"FINISHED"}


class VIEW3D_PT_three_d_printing_tools(bpy.types.Panel):
    bl_label = "3D Printing Tools"
    bl_idname = "VIEW3D_PT_three_d_printing_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '3D Printing Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.remove_irregular_faces", text="Remove irregular faces")


classes = (
    OBJECT_OT_remove_irregular_faces,
    VIEW3D_PT_three_d_printing_tools,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
