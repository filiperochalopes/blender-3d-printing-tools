import bpy


def can_select_non_manifold_edges(context=None):
    context = context or bpy.context
    active_object = context.active_object
    return active_object is not None and active_object.type == 'MESH'


def select_non_manifold_edges(context=None):
    context = context or bpy.context
    active_object = context.active_object

    if active_object is None or active_object.type != 'MESH':
        return {"success": False, "active_object": None}

    if context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_non_manifold()

    return {"success": True, "active_object": active_object.name}
