Demonstration of the basics of delete - resoluation asymmetric tautology (DRAT)
proof verification using [Schur's Theorem for
r=2](https://proofwiki.org/wiki/Schur%27s_Theorem_%28Ramsey_Theory%29), which I
naively originally called the Boolean sum triples (BST) problem. This problem
asks whether the set of numbers _{1, ..., n}_ can be divided into two subsets
where neither subset contains the entire triple _(a, b, c)_ where _a=b+c_ and
_a<b<c_.

You can read my blog post that this is supporting material to
[here](https://ashgillman.github.io/2018/01/12/boolean-Pythagorean-triples.html).

See also https://www.cs.utexas.edu/~marijn/ptn/#example

[main.py](./main.py) contains the example.
The output of this file is:

    $ ./main.py
    Brute force
    3 : 1 2
            3

    4 : 1 2   4
            3

    5 : 1 2   4
            3   5

    6 : 1 2   4
            3   5 6

    7 : 1 2   4     7
            3   5 6

    8 : 1 2   4       8
            3   5 6 7

    9 : no solutions

    10 : no solutions

    Checking DRAT solution
    For n=3: not UNSAT
    For n=4: not UNSAT
    For n=5: not UNSAT
    For n=6: not UNSAT
    For n=7: not UNSAT
    For n=8: not UNSAT
    For n=9: UNSAT
    For n=10: UNSAT

`bst_plain_*.cnf` contain the DIMACS-encoded formulae for the BST problems from
`n=3` through `n=10`.
