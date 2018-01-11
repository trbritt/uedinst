
import unittest
from contextlib import suppress
from random import random
from time import sleep

from .. import ILS250PP, InstrumentException

HAS_STAGE = False
with suppress(InstrumentException):
    ILS250PP()
    HAS_STAGE = True

def random_pos():
    """ Return a random position for the ILS250PP stage. """
    return round(random(), ndigits = 3)

@unittest.skipIf(not HAS_STAGE, 'ILS250PP delay stage not connected.')
class TestILS250PP(unittest.TestCase):
    
    def test_absolute_move(self):
        """ Test that moving the stage correctly updates its position """
        new_pos = random_pos()
        with ILS250PP() as delay_stage:
            delay_stage.absolute_move(new_pos)
            target = delay_stage.target_position()
            curr_pos = delay_stage.current_position()
        self.assertAlmostEqual(curr_pos, new_pos, places = 2)
    
    def test_relative_move(self):
        """ Test that moving the stage relatively is working correctly """
        start = random_pos()
        move = random_pos()
        with ILS250PP() as delay_stage:
            delay_stage.absolute_move(start)
            delay_stage.relative_move(move)
            curr_pos = delay_stage.current_position()
        
        self.assertAlmostEqual(curr_pos, start + move, places = 2)
    
    def test_relative_time_shift(self):
        """ Test that the relative_time_shift() method moves by an
        appropriate amount """
        # Expected distance for 30 ps
        # recall that the stage moving by x means that the
        # path length changes by 2x
        expected = (30e-12) * 3e8 / 2 * 1e3 # ~ 4.5 mm
        
        with ILS250PP() as delay_stage:
            delay_stage.absolute_move(0.0)
            delay_stage.relative_time_shift(30)
            new_pos = delay_stage.current_position()
        
        self.assertAlmostEqual(new_pos, expected, places = 2)

if __name__ == '__main__':
    unittest.main()