# -*- coding: utf-8 -*-

__author__ = 'Hans E Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

import pytest
from scipy.stats import binom_test
from biolab.dish import Dish
from biolab.bacteria import Bacteria

# acceptance limit for statistical tests
ALPHA = 0.001


def test_dish_create():
    d = Dish(10, 20)
    assert d.get_num_a() == 10
    assert d.get_num_b() == 20


class TestAgingCalls:
    """
    Tests that Dish.aging() makes the correct number of calls
    to Bacteria.ages().
    """

    def test_dish_ages(self, mocker):
        # mocker.spy wraps Bacteria.ages() so that we can get
        # a call count (and more information if we wanted)
        mocker.spy(Bacteria, 'ages')

        n_a, n_b = 10, 20
        d = Dish(n_a, n_b)
        d.aging()

        assert Bacteria.ages.call_count == n_a + n_b

    def test_dish_ages_callers(self, mocker):
        # mocker.spy wraps Bacteria.ages() so that we can get
        # a list of arguments for all calls to ages()
        mocker.spy(Bacteria, 'ages')

        n_a, n_b = 10, 20
        d = Dish(n_a, n_b)
        d.aging()

        # get list of arguments for each call
        # each element of the list is a tuple: (positional_args, kwargs)
        # ages() takes only self as positional arg, so we are only
        # interested in those
        args = Bacteria.ages.call_args_list
        pos_args, kwargs = zip(*args)

        # pos_args should be n_a + n_b different bacteria objects
        # use set() to eliminate duplicates
        assert len(set(pos_args)) == len(pos_args)


# The following parameterization ensures that all tests in
# the class run with (n_a, n_b)==(10, 20) and ==(30, 40)
@pytest.mark.parametrize('n_a, n_b', [(10, 20), (30, 40)])
class TestDeathDivision:
    """
    Tests for death and division.

    The main point of this test class is to show the use of a fixture
    to create an initial population before each test.
    """

    @pytest.fixture(autouse=True)
    def create_dish(self, n_a, n_b):
        """Create dish with bacteria numbers supplied by fixture."""
        self.n_a = n_a
        self.n_b = n_b
        self.dish = Dish(self.n_a, self.n_b)

    @pytest.fixture
    def reset_bacteria_defaults(self):
        # no setup
        yield

        # reset class parameters to default values after each test
        Bacteria.set_params(Bacteria.default_params)

    def test_death(self):
        n_a_old = self.dish.get_num_a()
        n_b_old = self.dish.get_num_b()

        for _ in range(10):
            self.dish.death()
            n_a = self.dish.get_num_a()
            n_b = self.dish.get_num_b()
            # n_a and n_b must never increase
            assert n_a <= n_a_old
            assert n_b <= n_b_old
            n_a_old, n_b_old = n_a, n_b

        # after 10 rounds of death probability of no change is minimal
        assert self.dish.get_num_a() < self.n_a
        assert self.dish.get_num_b() < self.n_b

    def test_division(self):
        n_a_old = self.dish.get_num_a()
        n_b_old = self.dish.get_num_b()

        for _ in range(10):
            self.dish.division()
            n_a = self.dish.get_num_a()
            n_b = self.dish.get_num_b()
            # n_a and n_b must never decrease
            assert n_a >= n_a_old
            assert n_b >= n_b_old
            n_a_old, n_b_old = n_a, n_b

        # after 10 rounds of death probability of no change is minimal
        assert self.dish.get_num_a() > self.n_a
        assert self.dish.get_num_b() > self.n_b

    def test_all_die(self, reset_bacteria_defaults):
        Bacteria.set_params({'p_death': 1.0})
        self.dish.death()
        assert self.dish.get_num_a() == 0
        assert self.dish.get_num_b() == 0

    # Each value for p_death will be combined with each value
    # of (n_a, n_b)
    @pytest.mark.parametrize('p_death', [0.1, 0.9, 0.5])
    def test_death(self, reset_bacteria_defaults, p_death):

        Bacteria.set_params({'p_death': p_death})
        n_a0 = self.dish.get_num_a()
        n_b0 = self.dish.get_num_b()
        self.dish.death()
        died_a = n_a0 - self.dish.get_num_a()
        died_b = n_b0 - self.dish.get_num_b()

        assert binom_test(died_a, n_a0, p_death) > ALPHA
        assert binom_test(died_b, n_b0, p_death) > ALPHA
