import bmesh
import bpy


def _selected_mesh_objects(context):
    return [obj for obj in context.selected_objects if obj.type == 'MESH']


def _triangulate_irregular_faces(obj):
    bm = bmesh.new()

    try:
        bm.from_mesh(obj.data)
        irregular_faces = [face for face in bm.faces if len(face.verts) > 4]
        irregular_faces_count = len(irregular_faces)

        if irregular_faces_count:
            bmesh.ops.triangulate(bm, faces=irregular_faces)
            bm.to_mesh(obj.data)
            obj.data.update()

        return irregular_faces_count
    finally:
        bm.free()


def remove_irregular_faces(context=None):
    context = context or bpy.context
    selected_objects = _selected_mesh_objects(context)

    if not selected_objects:
        print("Nenhum objeto de malha selecionado.")
        return {"processed_objects": 0, "corrected_faces": 0, "objects": []}

    processed_objects = []
    corrected_faces = 0

    for obj in selected_objects:
        print(f"Processando: {obj.name}")
        corrected = _triangulate_irregular_faces(obj)

        if corrected:
            print(f"-> {corrected} faces irregulares corrigidas em {obj.name}")
        else:
            print(f"-> {obj.name} já está limpo.")

        processed_objects.append({"name": obj.name, "corrected_faces": corrected})
        corrected_faces += corrected

    print("Processo concluído!")
    return {
        "processed_objects": len(selected_objects),
        "corrected_faces": corrected_faces,
        "objects": processed_objects,
    }


def triangular_selecao(context=None):
    return remove_irregular_faces(context)


if __name__ == "__main__":
    triangular_selecao(bpy.context)
