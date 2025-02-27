'''
Created on May 30, 2019
@author: Andrew Habib
'''

import unittest
import warnings

from jsonschema.exceptions import SchemaError

from jsonsubschema.checker import isSubschema


class TestIntegerSubtype(unittest.TestCase):

    def test_identity(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = s1
        self.assertTrue(isSubschema(s1, s2))

    def test_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 1}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_max_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_max_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 1, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 10, "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_min_max3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 40, "maximum": 100}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_xmax(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_xmin_xmax1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 6, "maximum": 19}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_xmin_xmax2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 6, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_xmin_xmax(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": False, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_mulOf1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 98}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10, "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10, "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 500}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_mul(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 10, "multipleOf": 15}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestNumberSubtype(unittest.TestCase):

    def test_identity(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        s2 = s1
        self.assertTrue(isSubschema(s1, s2))

    def test_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 1}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_max_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "maximum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_max_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 1, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 10, "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_min_max3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 40, "maximum": 100}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "exclusiveMinimum": True, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_xmax(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "exclusiveMinimum": True, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_xmin_xmax1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 6, "maximum": 19}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_xmin_xmax2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 6, "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_xmin_xmax(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "exclusiveMinimum": False, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_mulOf1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 10.5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 1.5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 6}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_mulOf3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": .5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": -.5}
        self.assertRaises(SchemaError, isSubschema, s1, s2)

    def test_mulOf4(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 1}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 10, "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 10, "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 5, "maximum": 500}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestNumericSubtype(unittest.TestCase):

    def test_int_num(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_num_int(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 1.5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_num_min_int(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_num_int(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_num_int2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 1}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestCompositeNumericSubtype(unittest.TestCase):

    def test_invalid_schema(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number",
              "allOf": [""]}
        with self.subTest():
            self.assertRaises(SchemaError, isSubschema, s1, s2)
        with self.subTest():
            self.assertRaises(SchemaError, isSubschema, s2, s1)

    def test_int_int_num1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number",
              "allOf": [{"type": "integer"}, {"type": "number", "minimum": 10}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_int_int_num2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number",
              "allOf": [{"type": "integer"}, {"type": "number", "minimum": 10}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_int_mul_mul1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number",
              "multipleOF": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 3}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_int_mul_mul2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 15}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number",
              "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 5}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_all_all_1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema", "type": "integer",
              "allOf": [{"multipleOf": 3}, {"minimum": 5}]}  # 6, 9, 12, 15, 18, ...
        s2 = {"$schema": "http://json-schema.org/draft-04/schema", "type": "number", "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 5}]}  # ..., -30, -15, 15, 30, 45, ..
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_all_all_2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer",
              "allOf": [{"multipleOf": 3}]}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 3}]}  # ..., -30, -15, 15, 30, 45, ..
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_all_all_3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "allOf": [{"multipleOf": .3}]}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 3}]}  # ..., -30, -15, 15, 30, 45, ..
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))
