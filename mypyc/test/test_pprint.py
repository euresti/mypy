import unittest
from typing import List

from mypyc.ir.ops import BasicBlock, Register, Op, LoadInt, BinaryIntOp, Unreachable, Assign
from mypyc.ir.rtypes import int_rprimitive
from mypyc.ir.pprint import generate_names_for_env


def register(name: str) -> Register:
    return Register(int_rprimitive, 'foo', is_arg=True)


def make_block(ops: List[Op]) -> BasicBlock:
    block = BasicBlock()
    block.ops.extend(ops)
    return block


class TestGenerateNames(unittest.TestCase):
    def test_empty(self) -> None:
        assert generate_names_for_env([], []) == {}

    def test_arg(self) -> None:
        reg = register('foo')
        assert generate_names_for_env([reg], []) == {reg: 'foo'}

    def test_int_op(self) -> None:
        op1 = LoadInt(2)
        op2 = LoadInt(4)
        op3 = BinaryIntOp(int_rprimitive, op1, op2, BinaryIntOp.ADD)
        block = make_block([op1, op2, op3, Unreachable()])
        assert generate_names_for_env([], [block]) == {op1: 'i0', op2: 'i1', op3: 'r0'}

    def test_assign(self) -> None:
        reg = register('foo')
        op1 = LoadInt(2)
        op2 = Assign(reg, op1)
        op3 = Assign(reg, op1)
        block = make_block([op1, op2, op3])
        assert generate_names_for_env([reg], [block]) == {op1: 'i0', reg: 'foo'}
