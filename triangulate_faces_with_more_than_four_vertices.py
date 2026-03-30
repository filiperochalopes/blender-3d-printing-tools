import bpy
import bmesh

def triangular_selecao():
    # Pega apenas os objetos que você selecionou e que são malhas (MESH)
    objetos_selecionados = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    if not objetos_selecionados:
        print("Nenhum objeto de malha selecionado.")
        return

    for obj in objetos_selecionados:
        print(f"Processando: {obj.name}")
        
        # Define o objeto como ativo para entrar no modo de edição
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Cria o BMesh para manipular a geometria
        bm = bmesh.from_edit_mesh(obj.data)

        # Filtra apenas faces com mais de 4 vértices (N-gons)
        ngons = [f for f in bm.faces if len(f.verts) > 4]

        if ngons:
            # Triangula somente as faces identificadas
            bmesh.ops.triangulate(bm, faces=ngons)
            print(f"-> {len(ngons)} N-gons corrigidos em {obj.name}")
        else:
            print(f"-> {obj.name} já está limpo.")

        # Salva as alterações e volta para o Object Mode
        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')

    print("Processo concluído!")

# Executa a função
triangular_selecao()
