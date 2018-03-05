#!/usr/bin/env python3

import copy
import itertools


bst_refutation = [
    [1, 4],
    [1],
    [4],
    [],
]

eg_cnf = [
    [ 1, 2, -3], [-1, -2,  3],
    [ 2, 3, -4], [-2, -3,  4],
    [ 1, 3,  4], [-1, -3, -4],
    [-1, 2,  4], [ 1, -2, -4]]

eg_drat = [
    [-1],
    [2],
    [],
]


def unique(list_):
    unique = []
    [unique.append(l) for l in list_ if l not in unique]
    return unique


def negate_clause(c):
    """Conjuction of unit clauses that falsify literals in C"""
    return [[-l] for l in c]


def write_cnf(n, cnf, filename):
    with open(filename, 'w+') as out:
        print('p', 'cnf', n, len(cnf),
              file=out)

        for clause in cnf:
            print(*clause, 0, file=out)


def read_cnf(filename):
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
    # print(n, cnf)
    for solution in itertools.product((True, False), repeat=n):
        # print('check solution:', solution)
        sat = True
        for clause in cnf:
            # print('clause:', clause)
            if not clause:
                # print('empty clause')
                sat = False
                break
            clause_eval = (solution[abs(c) - 1] for c in clause)
            clause_eval = list(clause_eval)
            clause_eval = (e if c >= 0 else not e
                           for c, e in zip(clause, clause_eval))
            # clause_eval = list(clause_eval)
            # print('eval to:', clause_eval)
            if not any(clause_eval):
                # print('failed')
                sat = False
                break
            # print('passed')

        if sat:
            return solution
    return False


def unit_propagate(cnf):
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
    assert unit_propagate([[1, 2], [1]]) == [[1]]
    assert unit_propagate([[-1, 2], [1]]) == [[2], [1]]
    # http://www.dis.uniroma1.it/~liberato/ar/incomplete/incomplete.html
    # {x, ¬x ∨ ¬y, x ∨ ¬z, y ∨ z, y ∨ ¬z}
    # [[1], [-1, -2], [1, -3], [2, 3], [2, -3]]
    # [[1], [-2], [2, 3], [2, -3]]
    # [[1], [-2], [3], [-3]]
    # [[1], [-2], []]
    assert unit_propagate([[1], [-1, -2], [1, -3], [2, 3], [2, -3]]) \
        == [[1], [-2], []]


def test_verify_drat():
    assert verify_drat(eg_cnf, eg_drat)
    assert not verify_drat(eg_cnf, [])
    assert not verify_drat(eg_cnf, eg_drat[:-2])

    assert not verify_drat(encode_bst(8), bst_refutation)
    assert verify_drat(encode_bst(9), bst_refutation)
    assert verify_drat(encode_bst(10), bst_refutation)
    assert not verify_drat(encode_bst(9), eg_drat)


if __name__ == '__main__':
    test_unit_propagate()
    test_verify_drat()

    print('Brute force')
    for n in range(3, 10 + 1):
        cnf = encode_bst(n)
        solution = brute_force(n, cnf)
        if solution:
            print(n, ':', *('{:2}'.format(i+1) if solution[i] else '  '
                            for i in range(n)))
            print(' ', ' ', *('{:2}'.format(i+1) if not solution[i] else '  '
                            for i in range(n)))
        else:
            print(n, ': no solutions')
        print()

    print('Checking DRAT solution')
    print('For n=8:',
          'SAT' if verify_drat(encode_bst(8), bst_refutation) else 'UNSAT')
    print('For n=9:',
          'SAT' if verify_drat(encode_bst(9), bst_refutation) else 'UNSAT')
