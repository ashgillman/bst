Demonstration of the basics of delete - resoluation asymmetric tautology
(DRAT) proof verification using the Boolean sum triples (BST) problem. This
problem asks whether the set of numbers _{1, ..., n}_ can be divided into two
subsets where neither subset contains the entire triple _(a, b, c)_ where _a=b+c_
and _a<b<c_.

See https://www.cs.utexas.edu/~marijn/ptn/#example

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
