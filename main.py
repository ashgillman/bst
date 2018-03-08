#!/usr/bin/env python3
"""Demonstration of the basics of delete - resoluation asymmetric tautology
(DRAT) proof verification using Schur's Theorem for r=2, which I naively
originally called the Boolean sum triples (BST) problem. This problem asks
whether the set of numbers {1, ..., n} can be divided into two subsets where
neither subset contains the entrire triple (a, b, c) where a=b+c and a<b<c.

See https://www.cs.utexas.edu/~marijn/ptn/#example

"""

import copy
import itertools


# DRAT refutation proof for BST (n >= 9)
bst_refutation = [
    [1, 4],
    [1],
    [4],
    [],
]

# Another example problem in conjugate normal form (CNF) from
eg_cnf = [
    [ 1, 2, -3], [-1, -2,  3],
    [ 2, 3, -4], [-2, -3,  4],
    [ 1, 3,  4], [-1, -3, -4],
    [-1, 2,  4], [ 1, -2, -4]]

# DRAT proof of unsatisfiability of the example problem above
eg_drat = [
    [-1],
    [2],
    [],
]


def unique(list_):
    """Eliminate duplicates in a list."""
    unique = []
    [unique.append(l) for l in list_ if l not in unique]
    return unique


def negate_clause(c):
    """Conjuction of unit clauses that falsify literals in C"""
    return [[-l] for l in c]


def write_cnf(n, cnf, filename):
    """Save a formula in conjugate normal form (CNF) to DIMACS format."""
    with open(filename, 'w+') as out:
        print('p', 'cnf', n, len(cnf),
              file=out)

        for clause in cnf:
            print(*clause, 0, file=out)


def read_cnf(filename):
    """Load a formula in conjugate normal form (CNF) from DIMACS format."""
    with open(filename, 'r') as in_:
        _, _, n, _ = in_.readline().strip().split()
        n = int(n)

        cnf = []
        for clause in in_.readlines():
            cnf.append(tuple(int(i) for i in clause))

    return n, cnf


def encode_bst(n):
    """Encodes the Boolean Sum Triples up to n in DIMACS CNF format."""
    cnf = []
    for a in range(1, n - 1):
        for b in range(a + 1, n - a + 1):
            c = a + b
            cnf.append([a, b, c])
            cnf.append([-a, -b, -c])

    out_f = 'bst_plain_{}.cnf'.format(n)
    write_cnf(n, cnf, out_f)

    return cnf


def brute_force(n, cnf):
    """Check entire solution space to solve satisfiability of a formula."""
    # solution space is all possible values of the n variables (i.e., 2**n)
    solution_space = itertools.product((True, False), repeat=n)
    for solution in solution_space:
        sat = True  # until proven otherwise
        for clause in cnf:
            if not clause:  # if empty clause in formula
                sat = False
                break
            clause_eval = (solution[abs(c) - 1] for c in clause)
            clause_eval = list(clause_eval)
            clause_eval = (e if c >= 0 else not e
                           for c, e in zip(clause, clause_eval))
            if not any(clause_eval):  # if clause evaluates for False
                sat = False
                break
            # otherwise the current clause is satisfiable, on to the next

        if sat:
            return solution

    # checked all solution_space and found no solutions
    return False


def unit_propagate(cnf):
    """Apply unit propagation of all unit clauses to remaining causes.

    In the case a conflict is derived, both conflicts are eliminated and the
    formula will contain an empty clause
    """
    cnf = copy.deepcopy(cnf)  # we are going to modify in place

    reached_fixpoint = False
    while not reached_fixpoint:
        reached_fixpoint = True  # until proven otherwise

        # get units to propagate
        units = [c[0] for c in cnf if len(c) == 1]

        # propagate reduncancies
        for l in units:
            for c in cnf:
                if l in c and len(c) > 1:
                    # remove redundant clause c
                    cnf.remove(c)
                    reached_fixpoint = False
                elif -l in c:
                    # remove reduncant literal l
                    c.remove(-l)
                    reached_fixpoint = False

    return unique(cnf)


def has_RAT(formula, clause, pivot):
    """Determine if a clause has resoluation asymmetric tautology (RAT) on the
    pivot w.r.t the formula.

    See definition 1 in Solving and Verifying the boolean Pythagorean Triples
    problem via Cube-and-Conquer by Marijn J.H. Heule, Oliver Kullmann, and
    Victor Marek
    https://arxiv.org/abs/1605.00723
    """
    assert pivot in clause

    Ds = [c for c in formula if -pivot in c]
    Ds_without_xbar = [[l for l in c if l != -pivot] for c in Ds]
    unit_propagated = [
        unit_propagate(formula
                       + negate_clause(unique(clause + D_without_xbar)))
        for D_without_xbar in Ds_without_xbar]
    derives_confict = [[] in x for x in unit_propagated]
    return all(derives_confict)


def verify_drat(cnf, drat):
    """Check that all clauses in a proof, drat, have RAT w.r.t the formula,
    cnf, and that the proof derives a conflict."""
    cnf = copy.deepcopy(cnf)  # we are going to modify in place

    for drat_clause in drat:
        if drat_clause:
            if has_RAT(cnf, drat_clause, drat_clause[0]):
                cnf.append(drat_clause)
            else:
                return False
        else:
            # empty, must be done
            break
    return [] in unit_propagate(cnf)


def test_unit_propagate():
    """This is NOT a rigorous test that unit_propagate is correct..."""
    assert unit_propagate([[1, 2], [1]]) == [[1]]
    assert unit_propagate([[-1, 2], [1]]) == [[2], [1]]
    # http://www.dis.uniroma1.it/~liberato/ar/incomplete/incomplete.html
    # {x, ¬x ∨ ¬y, x ∨ ¬z, y ∨ z, y ∨ ¬z}
    # [[1], [-1, -2], [1, -3], [2, 3], [2, -3]]
    # eliminate [1, ...] and -1
    # [[1], [-2], [2, 3], [2, -3]]
    # eliminate [-2, ...] and 2
    # [[1], [-2], [3], [-3]]
    # eliminate 3 and -3 to derive a conflict (empty clause)
    # [[1], [-2], []]
    assert unit_propagate(
        [[1], [-1, -2], [1, -3], [2, 3], [2, -3]]) \
        == [[1], [-2], []]


def test_verify_drat():
    """This is NOT a rigorous test that verify_drat is correct..."""
    assert verify_drat(eg_cnf, eg_drat), 'Example in paper works'
    assert not verify_drat(eg_cnf, []), "Empty proof doesn't work"
    assert not verify_drat(eg_cnf, [[1, 2], [3, 4]]), \
        "Silly proof doesn't work"
    assert not verify_drat(eg_cnf, eg_drat[:-2]), \
        "Incomplete proof doesn't work"

    assert not verify_drat(encode_bst(8), bst_refutation), \
        "SAT problem isn't proven UNSAT"
    assert verify_drat(encode_bst(9), bst_refutation), \
        'Presented solution to BST works'
    assert verify_drat(encode_bst(10), bst_refutation), \
        'Presented solution to BST works on larger problem'
    assert not verify_drat(encode_bst(9), eg_drat), \
        "Valid proof for another problem doesn't work on this problem"


if __name__ == '__main__':
    test_unit_propagate()
    test_verify_drat()

    print('Brute force')
    for n in range(3, 10 + 1):
        cnf = encode_bst(n)
        solution = brute_force(n, cnf)
        if solution:
            print(n, ':',
                  *(i + 1 if solution[i] else ' ' for i in range(n)))
            print(' ', ' ',
                  *(i + 1 if not solution[i] else ' ' for i in range(n)))
        else:
            print(n, ': no solutions')
        print()

    print('Checking DRAT solution')
    for n in range(3, 10 + 1):
        print('For n={}:'.format(n),
              'UNSAT'
              if verify_drat(encode_bst(n), bst_refutation)
              else 'not UNSAT')
