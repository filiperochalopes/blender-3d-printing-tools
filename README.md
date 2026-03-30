# 3D Printing Tools

`3D Printing Tools` é a base inicial de um add-on para Blender voltado à preparação de modelos para impressão 3D.

O repositório de referência analisado foi `/Users/filipelopes/Desktop/Web/Progress/blender-cortecloud-export-extension`, que já possui estrutura de extensão Blender com manifesto, organização de add-on e empacotamento. Neste repositório atual, a proposta é iniciar uma versão nova, focada em utilitários para impressão 3D.

## Objetivo

Construir um add-on que concentre verificações e correções comuns antes da exportação de peças para impressão 3D, reduzindo etapas manuais no fluxo dentro do Blender.

## Estado Atual

O repositório já foi organizado como base de add-on Blender:

- `__init__.py`: registro do add-on, operador e painel lateral
- `utils/`: ponto de organização para utilitários reutilizáveis
- `utils/irregular_faces.py`: logica do primeiro utilitario, reaproveitada pelo botao do painel

O primeiro botao do add-on e `Solve irregular faces`, que triangula faces com mais de quatro vertices nos objetos de malha selecionados.

## Escopo Inicial do Add-on

As primeiras capacidades previstas para `3D Printing Tools` são:

- triangulação de N-gons em objetos selecionados
- criação rápida de Boolean modifiers entre objeto ativo e alvos selecionados
- aplicação em lote de modifiers nos objetos selecionados
- checagem de malhas para impressão 3D
- validação de escala e unidades da cena
- inspeção de normais e geometria não manifold
- ações rápidas de preparação antes da exportação

## Estrutura Atual

A estrutura inicial do projeto ficou assim:

- `__init__.py` para registro do add-on, operador e painel
- `utils/` para lógica reutilizável
- `utils/irregular_faces.py` com o primeiro fluxo funcional
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
6. clique em `Solve irregular faces`

Para Boolean:

1. selecione o objeto ativo que deve receber os modifiers
2. mantenha selecionados os demais objetos como targets
3. use os ícones da mesma linha para `Subtract`, `Intersect` ou `Union`
4. clique em `Apply modifiers` para aplicar, de cima para baixo, os modifiers dos objetos selecionados

## Build

```sh
blender --command extension validate
blender --command extension build
```

## Identidade Inicial

- Nome do add-on: `3D Printing Tools`
- ID da extensão: `three_d_printing_tools`
- Versão atual: `0.1.1`
