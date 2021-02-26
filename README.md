---
title: GitHub Workflow Template for Crytic Slither
description: Slither CI Pipeline workflow
version: v.1.0.0
---

# Slither scripts | Functions by modifier

Detect functions in any set of Solidity smart contract that are labeled with a given modifier, using [Slither](https://github.com/trailofbits/slither).

This script is based on [Slither's `contract-summary` printer](https://github.com/trailofbits/slither/blob/ff280c2b6f35f8df4efff92903700da7d04fb415/slither/printers/summary/contract.py#L13).

## Usage
`python modifier.py <contract.sol> <modifier-name>`

Example:
~~~
$ python modifier.py test/TestContract.sol firstModifier
== Functions with firstModifier modifier ==

+ Contract ParentContract

+ Contract TestContract
  - From TestContract
    - withTwoModifiers(address) (public)
    - withOneModifier() (internal)
~~~

## Limitations
Currently, the script does not look for modifiers in internal calls.
For instance, in the following code snippet, `foo` will not be listed as having the `onlyOwner` modifier, even though it actually is restricted by that modifier due to the internal call to `bar()`.

~~~solidity
contract Test {
    modifier onlyOwner() { ... }

    function foo() public {
        bar();
    }
    
    function bar() public onlyOwner { ... }
}
~~~




## Slither GitHub Actions Workflow

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
