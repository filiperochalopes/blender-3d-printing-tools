# 3D Printing Tools

`3D Printing Tools` é a base inicial de um add-on para Blender voltado à preparação de modelos para impressão 3D.

O repositório de referência analisado foi `/Users/filipelopes/Desktop/Web/Progress/blender-cortecloud-export-extension`, que já possui estrutura de extensão Blender com manifesto, organização de add-on e empacotamento. Neste repositório atual, a proposta é iniciar uma versão nova, focada em utilitários para impressão 3D.

## Objetivo

Construir um add-on que concentre verificações e correções comuns antes da exportação de peças para impressão 3D, reduzindo etapas manuais no fluxo dentro do Blender.

## Estado Atual

Hoje o repositório contém um utilitário isolado:

- `triangulate_faces_with_more_than_four_vertices.py`: triangula faces com mais de quatro vértices nos objetos de malha selecionados

Esse script serve como primeiro bloco funcional para a futura transformação em add-on instalável.

## Escopo Inicial do Add-on

As primeiras capacidades previstas para `3D Printing Tools` são:

- triangulação de N-gons em objetos selecionados
- checagem de malhas para impressão 3D
- validação de escala e unidades da cena
- inspeção de normais e geometria não manifold
- ações rápidas de preparação antes da exportação

## Estrutura Planejada

Uma estrutura inicial recomendada para o projeto é:

- `__init__.py` para registro do add-on
- `operators/` para operadores Blender
- `panels/` para interface no `View3D`
- `utils/` para lógica reutilizável
- `blender_manifest.toml` para empacotamento como extensão

## Próximos Passos

1. transformar o script de triangulação em operador Blender
2. criar `__init__.py` com `bl_info`, registro e painel inicial
3. adicionar interface no painel lateral com ações de preparação
4. organizar o código em módulos reutilizáveis
5. validar e empacotar a extensão com o manifesto

## Build

```sh
blender --command extension validate
blender --command extension build
```

## Identidade Inicial

- Nome do add-on: `3D Printing Tools`
- ID da extensão: `three_d_printing_tools`
- Versão inicial: `0.1.0`
