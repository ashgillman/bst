#!/usr/bin/env python3

import itertools


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
            cnf.append((a, b, c))
            cnf.append((-a, -b, -c))

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


if __name__ == '__main__':
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
