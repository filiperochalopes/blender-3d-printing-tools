# 3D Printing Tools

`3D Printing Tools` é a base inicial de um add-on para Blender voltado à preparação de modelos para impressão 3D.

O repositório de referência analisado foi `/Users/filipelopes/Desktop/Web/Progress/blender-cortecloud-export-extension`, que já possui estrutura de extensão Blender com manifesto, organização de add-on e empacotamento. Neste repositório atual, a proposta é iniciar uma versão nova, focada em utilitários para impressão 3D.

## Objetivo

Construir um add-on que concentre verificações e correções comuns antes da exportação de peças para impressão 3D, reduzindo etapas manuais no fluxo dentro do Blender.

## Estado Atual

O repositório já foi organizado como base de add-on Blender:

- `__init__.py`: registro do add-on, operador e painel lateral
- `utils/`: ponto de organização para utilitários reutilizáveis
- `triangulate_faces_with_more_than_four_vertices.py`: lógica do primeiro utilitário, reaproveitada pelo botão do painel

O primeiro botão do add-on é `Remove irregular faces`, que triangula faces com mais de quatro vértices nos objetos de malha selecionados.

## Escopo Inicial do Add-on

As primeiras capacidades previstas para `3D Printing Tools` são:

- triangulação de N-gons em objetos selecionados
- checagem de malhas para impressão 3D
- validação de escala e unidades da cena
- inspeção de normais e geometria não manifold
- ações rápidas de preparação antes da exportação

## Estrutura Atual

A estrutura inicial do projeto ficou assim:

- `__init__.py` para registro do add-on, operador e painel
- `utils/` para lógica reutilizável
- `triangulate_faces_with_more_than_four_vertices.py` com o primeiro fluxo funcional
- `blender_manifest.toml` para empacotamento como extensão

## Próximos Passos

1. adicionar novos operadores de inspeção de malha
2. expandir o painel lateral com mais ferramentas de preparação
3. separar utilitários por domínio conforme o add-on crescer
4. validar e empacotar a extensão com o manifesto

## Como Usar

1. instale ou carregue o add-on no Blender
2. abra o `View3D`
3. vá à barra lateral direita
4. abra a aba `3D Printing Tools`
5. selecione um ou mais objetos do tipo `MESH`
6. clique em `Remove irregular faces`

## Build

```sh
blender --command extension validate
blender --command extension build
```

## Identidade Inicial

- Nome do add-on: `3D Printing Tools`
- ID da extensão: `three_d_printing_tools`
- Versão inicial: `0.1.0`
