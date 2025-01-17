from algebra.polynomials import * 
from utils.utils import *

class AIR():
    # w - register width, T - trace length; field = used base_field
    def __init__(self, w, T, field):
        #here we need to say, what does it mean to be a trace constraint
        self.w = w
        self.T = T
        self.field = field
        self.boundary_constraints = []
        self.trace_constraints = [None] * (T-1)
        self.vars = ['X' + str(i) for i in xrange(1, w+1)] + ['Y' + str(i) for i in xrange(1, w+1)]
        self.poly_ring = multiivar_polynomialsOver(field, *self.vars)
        self.variables = {}
        p = self.poly_ring
        for i in range(len(self.vars)):
            self.variables[p.variable_name] = p
            p = p.domain
        self.witness = None

    def set_witness(self, witness):
        self.witness = witness
    
    # boundary constraints are of the form (i, j, val), where 
    # i - number of step in trace from 0 to T
    # j - number of register from o to w
    # val - concrete value from field
    def add_boundary_constraint(self, i, j, val):
        assert (0 <= i < self.T), "specified value doesn't point to any correct step in execution trace"
        assert (0 <= j < self.w), "specified value  is not a register index" 
        self.boundary_constraints.append((i, j, self.field(val)))
    
    # trace constraints are of the form (i, poly), where
    # i - is the number of execution step
    # poly - polynomial in variables X1, .. X_w, Y_1, .. Y_w connecting registers between step i and i+1
    def add_trace_constraint(self, i, poly):
        assert (0 <= i < self.T - 1), "specified value doesn't point to any correct step in execution trace"
        # assert isinstance(poly, self.poly_ring), "specifed poly doesn't belong to underlying polynomial ring"
        self.trace_constraints[i] = poly

    # check if all constraints are defined at each execution step
    def consistency_check(self):
        if any([ elem is None for elem in self.trace_constraints]):
            return False
        if self.witness:
            return self.witness_check(self.witness)
        return True
    
    # check if provided witness satisfies all of the constraints
    # witness should be 2-dimensional matrix of size [T][w] 
    def witness_check(self, witness):
        for i, j, val in self.boundary_constraints:
            if witness[i][j] != val:
                return False
        for i, poly in enumerate(self.trace_constraints):
            if poly is not None:
                poly_copy = self.poly_ring(poly)
                p_val = poly_copy.evaluate(witness[i] + witness[i+1])
                if p_val != 0:
                    return False
        return True



