import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from algebra.finite_field import *
from algebra.polynomials import *
from relations.AIR import *

p = 17
Fp = IntegersModP(p, 3)

#import merklee tree
from merkle_tree.merkle_tree import *

def residue_field_hasher(x):
    x = hex(int(x))
    if x[-1] == "L":
        x = x[:-1]
    if len(x) % 2 !=0:
        x = "0" + x
    return x


tree_constructor = MerkleTreeFactory(leaf_encoder = residue_field_hasher, padding = Fp(0))

if __name__ == "__main__":
    num_registers = 2
    num_steps = 4
    air = AIR(num_registers, num_steps, Fp)
    air.add_boundary_constraint(0, 0, Fp(1))
    air.add_boundary_constraint(0, 1, Fp(1))
    air.add_boundary_constraint(3, 1, Fp(5))
    witness = [
        [1, 1],
        [1, 2],
        [2, 3],
        [3, 5],
    ]
    c0 = air.poly_ring.from_string("0 + X1 + X2 + 0*Y1 - Y2")
    c1 = air.poly_ring.from_string("0 + 0*X1 + X2 - Y1 + 0*Y2")

    air.add_trace_constraint(0, c0)
    # air.add_trace_constraint(0, c1)
    air.add_trace_constraint(1, c0)
    # air.add_trace_constraint(1, c1)
    air.add_trace_constraint(2, c0)
    # air.add_trace_constraint(2, c1)
    assert(air.witness_check(witness))
    air.set_witness(witness)
    assert(air.consistency_check())
    print(air)








