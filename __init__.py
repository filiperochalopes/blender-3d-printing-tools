bl_info = {
    "name": "3D Printing Tools",
    "author": "Filipe Lopes",
    "version": (0, 1, 1),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > 3D Printing Tools",
    "description": "Utilities to prepare models for 3D printing",
    "category": "Object",
}

import bpy
from bpy.props import EnumProperty

from . import utils


class OBJECT_OT_remove_irregular_faces(bpy.types.Operator):
    bl_idname = "object.remove_irregular_faces"
    bl_label = "Solve irregular faces"
    bl_description = "Triangulate faces with more than four vertices on the selected mesh objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and any(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        result = utils.solve_irregular_faces(context)

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


class OBJECT_OT_select_non_manifold_edges(bpy.types.Operator):
    bl_idname = "object.select_non_manifold_edges"
    bl_label = "Select Non Manifold edges"
    bl_description = "Enter Edit Mode, switch to Edge Select, and select non-manifold edges"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return utils.can_select_non_manifold_edges(context)

    def execute(self, context):
        result = utils.select_non_manifold_edges(context)

        if not result["success"]:
            self.report({"WARNING"}, "Select one active mesh object")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Selected non-manifold edges on {result['active_object']}")
        return {"FINISHED"}


class OBJECT_OT_add_boolean_modifiers(bpy.types.Operator):
    bl_idname = "object.add_boolean_modifiers"
    bl_label = "Add boolean modifiers"
    bl_description = "Add Boolean modifiers to the active object using the other selected objects as targets"
    bl_options = {"REGISTER", "UNDO"}

    operation: EnumProperty(
        name="Operation",
        items=(
            ("DIFFERENCE", "Difference", "Subtract target objects from the active object"),
            ("INTERSECT", "Intersect", "Keep only the intersection with the target objects"),
            ("UNION", "Union", "Join the target objects with the active object"),
        ),
    )

    @classmethod
    def poll(cls, context):
        return utils.can_add_boolean_modifiers(context)

    def execute(self, context):
        result = utils.add_boolean_modifiers(context, self.operation)

        if result["added_modifiers"] == 0:
            self.report({"WARNING"}, "Select one active mesh object and at least one other mesh object as target")
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            f"Added {result['added_modifiers']} Boolean modifier(s) to {result['active_object']}",
        )
        return {"FINISHED"}


class OBJECT_OT_apply_modifiers(bpy.types.Operator):
    bl_idname = "object.apply_modifiers"
    bl_label = "Apply modifiers"
    bl_description = "Apply all modifiers from top to bottom on the selected mesh objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return utils.can_apply_modifiers(context)

    def execute(self, context):
        result = utils.apply_modifiers(context)

        if result["selected_objects"] == 0:
            self.report({"WARNING"}, "Select at least one mesh object")
            return {"CANCELLED"}

        if result["applied_modifiers"] == 0 and not result["failed_modifiers"]:
            self.report({"INFO"}, "No modifiers found on the selected objects")
            return {"FINISHED"}

        if result["failed_modifiers"]:
            self.report(
                {"WARNING"},
                f"Applied {result['applied_modifiers']} modifier(s) with {len(result['failed_modifiers'])} failure(s)",
            )
            return {"FINISHED"}

        self.report({"INFO"}, f"Applied {result['applied_modifiers']} modifier(s)")
        return {"FINISHED"}


class VIEW3D_PT_three_d_printing_tools(bpy.types.Panel):
    bl_label = "3D Printing Tools"
    bl_idname = "VIEW3D_PT_three_d_printing_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '3D Printing Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.remove_irregular_faces", text="Solve irregular faces")
        layout.operator("object.select_non_manifold_edges", text="Select Non Manifold edges")
        row = layout.row(align=True)

        subtract = row.operator(
            "object.add_boolean_modifiers",
            text="",
            icon="SELECT_SUBTRACT",
        )
        subtract.operation = "DIFFERENCE"

        intersect = row.operator(
            "object.add_boolean_modifiers",
            text="",
            icon="SELECT_INTERSECT",
        )
        intersect.operation = "INTERSECT"

        union = row.operator(
            "object.add_boolean_modifiers",
            text="",
            icon="SELECT_EXTEND",
        )
        union.operation = "UNION"

        row.operator("object.apply_modifiers", text="Apply modifiers")


classes = (
    OBJECT_OT_remove_irregular_faces,
    OBJECT_OT_select_non_manifold_edges,
    OBJECT_OT_add_boolean_modifiers,
    OBJECT_OT_apply_modifiers,
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
