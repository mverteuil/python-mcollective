#!/usr/bin/env python

import unittest
from mcollective import Filter

class TestFilter(unittest.TestCase):

    def test_init(self):
        f = Filter()
        self.assertEqual(f.cf_class, [])
        self.assertEqual(f.agent, [])
        self.assertEqual(f.identity, [])
        self.assertEqual(f.fact, [{},])

    def test_cf_class(self):
        f = Filter(cf_class='foo::bar')
        self.assertEqual(f.cf_class, 'foo::bar')
        self.assertEqual(
            f.dict()['cf_class'],
            ['foo::bar', ],
        )

    def test_agent(self):
        f = Filter(agent='smith')
        self.assertEqual(f.agent, 'smith')
        self.assertEqual(
            f.dict()['agent'],
            ['smith', ],
        )

    def test_identity(self):
        f = Filter(identity='the.bourne')
        self.assertEqual(f.identity, 'the.bourne')
        self.assertEqual(
            f.dict()['identity'],
            ['the.bourne', ],
        )

    def test_fact(self):
        f = Filter(fact={'country' : 'uk', })
        self.assertEqual(f.fact, {'country' : 'uk', })
        self.assertEqual(
            f.dict()['fact'],
            {'country' : 'uk', },
        )

    def test_add_fact(self):
        f = Filter()
        f.add_fact('country', 'us')
        self.assertEqual(f.fact, {'country' : 'us', })
        f.add_fact('processorcount', '4')
        self.assertEqual(f.fact, {
            'country' : 'us',
            'processorcount' : '4',
        })

    def test_empty_dict(self):
        f = Filter()
        d = f.dict()
        self.assertEqual(d, {
            'cf_class' : [],
            'agent' : [],
            'identity' : [],
            'fact' : [{}, ],
        })

    def test_full_dict(self):
        f = Filter(
            cf_class='foo::bar',
            agent='smith',
            identity='the.bourne',
            fact={ 'country' : 'uk', },
        )
        f.add_fact('processorcount', '4')
        d = f.dict()
        self.assertEqual(d, {
            'cf_class' : ['foo::bar', ],
            'agent' : ['smith', ],
            'identity' : ['the.bourne'],
            'fact' : [{
                'country' : 'uk',
                'processorcount' : '4',
            }],
        })


if __name__ == '__main__':
    unittest.main()
