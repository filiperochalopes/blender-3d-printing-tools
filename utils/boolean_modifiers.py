import bpy


BOOLEAN_OPERATION_LABELS = {
    "DIFFERENCE": "Subtract",
    "INTERSECT": "Intersect",
    "UNION": "Union",
}


def _selected_mesh_objects(context):
    return [obj for obj in context.selected_objects if obj.type == 'MESH']


def _boolean_targets(context):
    active_object = context.active_object
    return [obj for obj in _selected_mesh_objects(context) if obj != active_object]


def can_add_boolean_modifiers(context=None):
    context = context or bpy.context
    active_object = context.active_object

    if context.mode != 'OBJECT':
        return False

    if active_object is None or active_object.type != 'MESH':
        return False

    return len(_boolean_targets(context)) > 0


def add_boolean_modifiers(context=None, operation="DIFFERENCE"):
    context = context or bpy.context
    active_object = context.active_object

    if active_object is None or active_object.type != 'MESH':
        return {"added_modifiers": 0, "active_object": None, "targets": []}

    targets = _boolean_targets(context)
    created_modifiers = []

    for target in targets:
        modifier = active_object.modifiers.new(
            name=f"{BOOLEAN_OPERATION_LABELS[operation]} {target.name}",
            type='BOOLEAN',
        )
        modifier.operation = operation
        modifier.object = target

        if hasattr(modifier, "solver"):
            modifier.solver = 'EXACT'

        created_modifiers.append({"modifier": modifier.name, "target": target.name})

    return {
        "added_modifiers": len(created_modifiers),
        "active_object": active_object.name,
        "targets": created_modifiers,
    }


def can_apply_modifiers(context=None):
    context = context or bpy.context

    if context.mode != 'OBJECT':
        return False

    return any(obj.type == 'MESH' and len(obj.modifiers) > 0 for obj in context.selected_objects)


def _set_selection(context, active_object, selected_objects):
    bpy.ops.object.select_all(action='DESELECT')

    for obj in selected_objects:
        obj.select_set(True)

    context.view_layer.objects.active = active_object


def apply_modifiers(context=None):
    context = context or bpy.context
    selected_mesh_objects = _selected_mesh_objects(context)

    if not selected_mesh_objects:
        return {
            "selected_objects": 0,
            "applied_modifiers": 0,
            "failed_modifiers": [],
        }

    original_active = context.view_layer.objects.active
    original_selected = list(context.selected_objects)
    applied_modifiers = 0
    failed_modifiers = []

    try:
        for obj in selected_mesh_objects:
            modifier_names = [modifier.name for modifier in obj.modifiers]

            if not modifier_names:
                continue

            _set_selection(context, obj, [obj])

            for modifier_name in modifier_names:
                if obj.modifiers.get(modifier_name) is None:
                    continue

                try:
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    applied_modifiers += 1
                except RuntimeError as error:
                    failed_modifiers.append(
                        {
                            "object": obj.name,
                            "modifier": modifier_name,
                            "error": str(error),
                        }
                    )
    finally:
        if original_selected:
            restored_active = original_active if original_active in original_selected else original_selected[0]
            _set_selection(context, restored_active, original_selected)
        else:
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = None

    return {
        "selected_objects": len(selected_mesh_objects),
        "applied_modifiers": applied_modifiers,
        "failed_modifiers": failed_modifiers,
    }
