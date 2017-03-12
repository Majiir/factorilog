#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.buffering import Buffer
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


KEYWORDS = {}


class NetlistBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=re.compile('[\\t ]+', RE_FLAGS | re.DOTALL),
        nameguard=None,
        comments_re=None,
        eol_comments_re='#.*?$',
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(NetlistBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class NetlistParser(Parser):
    def __init__(
        self,
        whitespace=re.compile('[\\t ]+', RE_FLAGS | re.DOTALL),
        nameguard=None,
        comments_re=None,
        eol_comments_re='#.*?$',
        ignorecase=None,
        left_recursion=False,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=NetlistBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(NetlistParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @graken()
    def _start_(self):
        self._file_()
        self._check_eof()

    @graken()
    def _file_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._newline_()
                with self._option():
                    self._netline_()
                    self.name_last_node('Entities')
                self._error('no available options')
        self._closure(block0)
        with self._optional():
            self._token('||')

            def block3():
                with self._choice():
                    with self._option():
                        self._newline_()
                    with self._option():
                        self._metaline_()
                        self.name_last_node('Metadata')
                    self._error('no available options')
            self._closure(block3)
        self.ast._define(
            ['Entities', 'Metadata'],
            []
        )

    @graken()
    def _newline_(self):
        with self._choice():
            with self._option():
                self._pattern(r'[\r\n]+')
            with self._option():
                self._check_eof()
            self._error('expecting one of: [\\r\\n]+')

    @graken()
    def _netline_(self):
        with self._optional():
            self._netlist_()
            self.name_last_node('OutNets')
            self._token('<=')
        with self._optional():
            self._netlist_()
            self.name_last_node('InNets')
        self._token(':')
        self._descriptor_()
        self.name_last_node('Descriptor')
        with self._optional():
            self._token('|')
            self._ent_id_()
            self.name_last_node('ID')
        self.ast._define(
            ['Descriptor', 'ID', 'InNets', 'OutNets'],
            []
        )

    @graken()
    def _netlist_(self):

        def sep0():
            self._token(',')

        def block0():
            self._name_()
        self._positive_closure(block0, sep=sep0)

    @graken()
    def _name_(self):
        self._pattern(r'[A-Za-z_][A-Za-z0-9_]*')

    @graken()
    def _ent_id_(self):
        self._uint_()

    @graken()
    def _descriptor_(self):
        with self._choice():
            with self._option():
                self._decider_descriptor_()
            with self._option():
                self._constant_descriptor_()
            with self._option():
                self._arithmetic_descriptor_()
            with self._option():
                self._entity_descriptor_()
            self._error('no available options')

    @graken()
    def _decider_descriptor_(self):
        self._out_type_()
        self.name_last_node('OutType')
        self._signal_()
        self.name_last_node('OutSig')
        self._token('if')
        self._signal_()
        self.name_last_node('Op1')
        self._comparator_()
        self.name_last_node('Comparator')
        self._channel_()
        self.name_last_node('Op2')
        self.ast._define(
            ['Comparator', 'Op1', 'Op2', 'OutSig', 'OutType'],
            []
        )

    @graken()
    def _out_type_(self):
        with self._choice():
            with self._option():
                self._token('1')
            with self._option():
                self._token('@')
            self._error('expecting one of: 1 @')

    @graken()
    def _comparator_(self):
        with self._choice():
            with self._option():
                self._token('>')
            with self._option():
                self._token('=')
            with self._option():
                self._token('<')
            self._error('expecting one of: < = >')

    @graken()
    def _constant_descriptor_(self):

        def sep0():
            self._token(',')

        def block0():
            self._signal_with_value_()
        self._positive_closure(block0, sep=sep0)

    @graken()
    def _signal_with_value_(self):
        self._int_()
        self.name_last_node('Value')
        self._signal_()
        self.name_last_node('Signal')
        self.ast._define(
            ['Signal', 'Value'],
            []
        )

    @graken()
    def _arithmetic_descriptor_(self):
        self._signal_()
        self.name_last_node('OutSig')
        self._token('=')
        self._signal_()
        self.name_last_node('Op1')
        self._operator_()
        self.name_last_node('Operator')
        self._channel_()
        self.name_last_node('Op2')
        self.ast._define(
            ['Op1', 'Op2', 'Operator', 'OutSig'],
            []
        )

    @graken()
    def _operator_(self):
        with self._choice():
            with self._option():
                self._token('+')
            with self._option():
                self._token('-')
            with self._option():
                self._token('/')
            with self._option():
                self._token('*')
            self._error('expecting one of: * + - /')

    @graken()
    def _entity_descriptor_(self):
        self._factorio_name_()

    @graken()
    def _channel_(self):
        with self._choice():
            with self._option():
                self._signal_()
            with self._option():
                self._int_()
            self._error('no available options')

    @graken()
    def _signal_(self):
        with self._choice():
            with self._option():
                self._full_signal_()
            with self._option():
                self._alpha_signal_()
            with self._option():
                self._special_signal_()
            self._error('no available options')

    @graken()
    def _factorio_name_(self):
        self._pattern(r'[A-Za-z0-9\-]+')

    @graken()
    def _full_signal_(self):
        self._factorio_name_()

    @graken()
    def _alpha_signal_(self):
        self._pattern(r'[A-Z]')

    @graken()
    def _special_signal_(self):
        with self._choice():
            with self._option():
                self._token('each')
            with self._option():
                self._token('any')
            with self._option():
                self._token('all')
            self._error('expecting one of: all any each')

    @graken()
    def _metaline_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._ent_meta_()
                with self._option():
                    self._net_meta_()
                with self._option():
                    self._global_meta_()
                self._error('no available options')
        self.name_last_node('@')
        self._newline_()

    @graken()
    def _ent_meta_(self):
        self._ent_id_()
        self.name_last_node('ID')
        self._token('|')
        with self._group():
            with self._choice():
                with self._option():
                    self._float_()
                with self._option():
                    self._int_()
                self._error('no available options')
        self.name_last_node('X')
        with self._group():
            with self._choice():
                with self._option():
                    self._float_()
                with self._option():
                    self._int_()
                self._error('no available options')
        self.name_last_node('Y')
        with self._optional():
            self._direction_()
            self.name_last_node('Direction')
        self.ast._define(
            ['Direction', 'ID', 'X', 'Y'],
            []
        )

    @graken()
    def _direction_(self):
        with self._choice():
            with self._option():
                self._token('N')
            with self._option():
                self._token('S')
            with self._option():
                self._token('E')
            with self._option():
                self._token('W')
            self._error('expecting one of: E N S W')

    @graken()
    def _net_meta_(self):
        self._name_()
        self.name_last_node('WireName')
        self._token('|')
        self._wire_color_()
        self.name_last_node('Color')

        def block2():
            self._WIRE_()
            self.add_last_node_to_name('Wires')
        self._closure(block2)
        self.ast._define(
            ['Color', 'WireName'],
            ['Wires']
        )

    @graken()
    def _WIRE_(self):
        self._TERMINAL_()
        self.name_last_node('Terminals')
        self._token('-')
        self._TERMINAL_()
        self.name_last_node('Terminals')
        self.ast._define(
            ['Terminals'],
            []
        )

    @graken()
    def _wire_color_(self):
        with self._choice():
            with self._option():
                self._token('red')
            with self._option():
                self._token('green')
            self._error('expecting one of: green red')

    @graken()
    def _TERMINAL_(self):
        self._ent_id_()
        self.name_last_node('ID')
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('i')
                with self._option():
                    self._token('o')
                with self._option():
                    self._token('p')
                self._error('expecting one of: i o p')
        self.name_last_node('Type')
        self.ast._define(
            ['ID', 'Type'],
            []
        )

    @graken()
    def _global_meta_(self):
        with self._choice():
            with self._option():
                self._global_name_()
            with self._option():
                self._global_icons_()
            self._error('no available options')

    @graken()
    def _global_name_(self):
        self._token('name')
        self._token('||')
        self._pattern(r'.*')
        self.name_last_node('Name')
        self.ast._define(
            ['Name'],
            []
        )

    @graken()
    def _global_icons_(self):
        self._token('icons')
        self._token('||')

        def block1():
            self._factorio_name_()
        self._positive_closure(block1)
        self.name_last_node('Names')
        self.ast._define(
            ['Names'],
            []
        )

    @graken('int')
    def _uint_(self):
        self._pattern(r'(0|[1-9][0-9]*)')

    @graken('int')
    def _int_(self):
        self._pattern(r'(0|[\-]?[1-9][0-9]*)')

    @graken('float')
    def _float_(self):
        self._pattern(r'[\-]?[0-9]*\.[0-9]+')


class NetlistSemantics(object):
    def start(self, ast):
        return ast

    def file(self, ast):
        return ast

    def newline(self, ast):
        return ast

    def netline(self, ast):
        return ast

    def netlist(self, ast):
        return ast

    def name(self, ast):
        return ast

    def ent_id(self, ast):
        return ast

    def descriptor(self, ast):
        return ast

    def decider_descriptor(self, ast):
        return ast

    def out_type(self, ast):
        return ast

    def comparator(self, ast):
        return ast

    def constant_descriptor(self, ast):
        return ast

    def signal_with_value(self, ast):
        return ast

    def arithmetic_descriptor(self, ast):
        return ast

    def operator(self, ast):
        return ast

    def entity_descriptor(self, ast):
        return ast

    def channel(self, ast):
        return ast

    def signal(self, ast):
        return ast

    def factorio_name(self, ast):
        return ast

    def full_signal(self, ast):
        return ast

    def alpha_signal(self, ast):
        return ast

    def special_signal(self, ast):
        return ast

    def metaline(self, ast):
        return ast

    def ent_meta(self, ast):
        return ast

    def direction(self, ast):
        return ast

    def net_meta(self, ast):
        return ast

    def WIRE(self, ast):
        return ast

    def wire_color(self, ast):
        return ast

    def TERMINAL(self, ast):
        return ast

    def global_meta(self, ast):
        return ast

    def global_name(self, ast):
        return ast

    def global_icons(self, ast):
        return ast

    def uint(self, ast):
        return ast

    def int(self, ast):
        return ast

    def float(self, ast):
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = NetlistParser()
    return parser.parse(text, startrule, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from grako.util import asjson

    ast = generic_main(main, NetlistParser, name='Netlist')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
