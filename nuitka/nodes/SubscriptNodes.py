#     Copyright 2016, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Subscript node.

Subscripts are important when working with lists and dictionaries. Tracking
them can allow to achieve more compact code, or predict results at compile time.

There is be a method "computeExpressionSubscript" to aid predicting them in the
other nodes.
"""

from .NodeBases import ExpressionChildrenHavingBase, StatementChildrenHavingBase


class StatementAssignmentSubscript(StatementChildrenHavingBase):
    kind = "STATEMENT_ASSIGNMENT_SUBSCRIPT"

    named_children = (
        "source",
        "expression",
        "subscript"
    )

    def __init__(self, expression, subscript, source, source_ref):
        StatementChildrenHavingBase.__init__(
            self,
            values     = {
                "source"     : source,
                "expression" : expression,
                "subscript"  : subscript
            },
            source_ref = source_ref
        )

    getSubscribed = StatementChildrenHavingBase.childGetter("expression")
    getSubscript = StatementChildrenHavingBase.childGetter("subscript")
    getAssignSource = StatementChildrenHavingBase.childGetter("source")

    def computeStatement(self, constraint_collection):
        result, change_tags, change_desc = self.computeStatementSubExpressions(
            constraint_collection = constraint_collection
        )

        if result is not self:
            return result, change_tags, change_desc

        subscribed = self.getSubscribed()
        subscript = self.getSubscript()
        source = self.getAssignSource()

        if subscribed.hasShapeDictionaryExact():
            from .ContainerOperationNodes import StatementDictOperationSet

            new_node = StatementDictOperationSet(
                dict_arg   = subscribed,
                key        = subscript,
                value      = source,
                source_ref = self.getSourceReference()
            )

            constraint_collection.removeKnowledge(subscribed)
            constraint_collection.removeKnowledge(subscript)
            constraint_collection.removeKnowledge(source)

            # Any code could be run, note that.
            constraint_collection.onControlFlowEscape(self)

            # Any exception may be raised.
            constraint_collection.onExceptionRaiseExit(BaseException)

            return new_node, "new_expression", """
Subscript assignment to dictionary lowered to dictionary assignment."""

        return subscribed.computeExpressionSetSubscript(
            set_node              = self,
            subscript             = subscript,
            value_node            = source,
            constraint_collection = constraint_collection
        )

    def getStatementNiceName(self):
        return "subscript assignment statement"


class StatementDelSubscript(StatementChildrenHavingBase):
    kind = "STATEMENT_DEL_SUBSCRIPT"

    named_children = (
        "expression",
        "subscript"
    )

    def __init__(self, expression, subscript, source_ref):
        StatementChildrenHavingBase.__init__(
            self,
            values     = {
                "expression" : expression,
                "subscript"  : subscript
            },
            source_ref = source_ref
        )

    getSubscribed = StatementChildrenHavingBase.childGetter("expression")
    getSubscript = StatementChildrenHavingBase.childGetter("subscript")

    def computeStatement(self, constraint_collection):
        result, change_tags, change_desc = self.computeStatementSubExpressions(
            constraint_collection = constraint_collection
        )

        if result is not self:
            return result, change_tags, change_desc

        subscribed = self.getSubscribed()
        subscript = self.getSubscript()

        return subscribed.computeExpressionDelSubscript(
            set_node              = self,
            subscript             = subscript,
            constraint_collection = constraint_collection
        )

    def getStatementNiceName(self):
        return "subscript del statement"


class ExpressionSubscriptLookup(ExpressionChildrenHavingBase):
    kind = "EXPRESSION_SUBSCRIPT_LOOKUP"

    named_children = (
        "subscribed",
        "subscript"
    )

    def __init__(self, subscribed, subscript, source_ref):
        ExpressionChildrenHavingBase.__init__(
            self,
            values     = {
                "subscribed" : subscribed,
                "subscript"  : subscript
            },
            source_ref = source_ref
        )

    getLookupSource = ExpressionChildrenHavingBase.childGetter("subscribed")
    getSubscript = ExpressionChildrenHavingBase.childGetter("subscript")

    def computeExpression(self, constraint_collection):
        return self.getLookupSource().computeExpressionSubscript(
            lookup_node           = self,
            subscript             = self.getSubscript(),
            constraint_collection = constraint_collection
        )

    def isKnownToBeIterable(self, count):
        return None
