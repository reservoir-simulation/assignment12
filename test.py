#!/usr/bin/env python

import numpy as np
import unittest

from assignment12 import *


class TestSolution(unittest.TestCase):

    def setUp(self):
        
        self.inputs = {
            'conversion factor': 6.33e-3,
            'fluid': {
                'water': {
                    'compressibility': 1e-6, #psi^{-1}
                    'viscosity': 1, #cp
                    'formation volume factor': 1,
                    },
            },
            'reservoir': {
                'permeability': 50, #mD
                'porosity': 0.2,
                'length': 10000, #ft
                'cross sectional area': 200000 #ft^2
            },
            'initial conditions': {
                'pressure': 1000 #psi
            },
            'boundary conditions': {
                'left': {
                    'type': 'prescribed pressure',
                    'value': 2000 #psi
                },
                'right': {
                    'type': 'prescribed flux',
                    'value': 0 #ft^3/day
                }
            },
            'numerical': {
                'solver': 'implicit',
                'number of grids': 4,
                'time step': 1, #day
                'number of time steps' : 3 
            },
            'plots': {
                'frequency': 1
            }
        }
    
        return 

    def test_compute_transmissibility(self):

        problem = OneDimReservoir(self.inputs)

        np.testing.assert_allclose(problem.compute_transmissibility(), 4000.0)

        return

    def test_compute_accumulation(self):

        problem = OneDimReservoir(self.inputs)

        np.testing.assert_allclose(problem.compute_accumulation(), 100.0)

        return 

    def test_is_transmissiblity_matrix_sparse(self):

        problem = OneDimReservoir(self.inputs)

        assert scipy.sparse.issparse(problem.T)

        return

    def test_implicit_solve_one_step(self):

        implicit = OneDimReservoir(self.inputs)
        implicit.solve_one_step()
        np.testing.assert_allclose(implicit.get_solution(), 
                                   np.array([1295.1463, 1051.1036, 1008.8921, 1001.7998]), 
                                   atol=0.5)
        return

    def test_explicit_solve_one_step(self):

        self.inputs['numerical']['solver'] = 'explicit'

        explicit = OneDimReservoir(self.inputs)

        explicit.solve_one_step()

        np.testing.assert_allclose(explicit.get_solution(), 
                               np.array([ 1506., 1000.,  1000.,  1000.004]), 
                               atol=0.5)
        return 

    def test_implicit_solve(self):

        implicit = OneDimReservoir(self.inputs)
        implicit.solve()
        np.testing.assert_allclose(implicit.get_solution(), 
                                   np.array([1582.9, 1184.8, 1051.5, 1015.9]), 
                                   atol=0.5)
        return

    def test_explicit_solve(self):

        self.inputs['numerical']['solver'] = 'explicit'

        explicit = OneDimReservoir(self.inputs)

        explicit.solve()

        np.testing.assert_allclose(explicit.get_solution(), 
                               np.array([1689.8, 1222.3, 1032.4, 1000.0]), 
                               atol=0.5)
        return 

    def test_mixed_method_solve_one_step_implicit(self):
        
        self.inputs['numerical']['solver'] = {'mixed method': {'theta': 0.0}}
        
        mixed_implicit = OneDimReservoir(self.inputs)
        
        mixed_implicit.solve_one_step()

        np.testing.assert_allclose(mixed_implicit.get_solution(), 
                               np.array([1295.1463, 1051.1036, 1008.8921, 1001.7998]), 
                               atol=0.5)
        return 

    def test_mixed_method_solve_one_step_explicit(self):
        
        self.inputs['numerical']['solver'] = {'mixed method': {'theta': 1.0}}
        
        mixed_explicit = OneDimReservoir(self.inputs)
        
        mixed_explicit.solve_one_step()

        np.testing.assert_allclose(mixed_explicit.get_solution(), 
                               np.array([ 1506., 1000.,  1000.,  1000.004]), 
                               atol=0.5)
        return 

    def test_mixed_method_solve_one_step_crank_nicolson(self):
        
        self.inputs['numerical']['solver'] = {'mixed method': {'theta': 0.5}}
        
        mixed = OneDimReservoir(self.inputs)
        
        mixed.solve_one_step()
        
        np.testing.assert_allclose(mixed.get_solution(), 
                                   np.array([ 1370.4,  1037.8 ,  1003.8,  1000.4]),
                                   atol=0.5)
        return 

    def test_mixed_method_solve_crank_nicolson(self):
            
                
        self.inputs['numerical']['solver'] = {'mixed method': {'theta': 0.5}}
                        
        mixed = OneDimReservoir(self.inputs)
                                
        mixed.solve()
                                        
        np.testing.assert_allclose(mixed.get_solution(), 
                                   np.array([ 1642.0,  1196.5,  1043.8,  1009.1]),
                                   atol=0.5)
    

if __name__ == '__main__':
        unittest.main()
