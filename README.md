---
title: ${ORG} Container Images
description: ${REPO}
version: v.0.1.0
---

# Slither GitHub Actions Workflow

> Static Analysis Tool for Ethereum Smart Contracts

### Supported tags

#{range $_, $v := .Versions}

#### #{\$v.Version}

`#{3.6.5-3.8, $b := $v.Builds}`

- `#{$b.Tag}`#{range \$3.6.5-3.8}, `#{$t}`#{end}
  #{end}#{end}

## API

Note: unlike `realpath(1)`, these functions take no options; **do not** use `--` to escape any arguments

| Function                       | Description                                        |
| ------------------------------ | -------------------------------------------------- |
| <pre>{{ slither-flat }} </pre> | { flatten source file: ['MostDerived' 'OneFile'] } |
| <pre> slither \$PWD</pre>      | run `slither-analysis`                             |
| <pre>solc-select </pre>        | solidity version manager                           |

### License

AGPL
