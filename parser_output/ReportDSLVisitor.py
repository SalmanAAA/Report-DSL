# Generated from ReportDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ReportDSLParser import ReportDSLParser
else:
    from ReportDSLParser import ReportDSLParser

# This class defines a complete generic visitor for a parse tree produced by ReportDSLParser.

class ReportDSLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ReportDSLParser#report_definition.
    def visitReport_definition(self, ctx:ReportDSLParser.Report_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#report_header.
    def visitReport_header(self, ctx:ReportDSLParser.Report_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#data_source_block.
    def visitData_source_block(self, ctx:ReportDSLParser.Data_source_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#filter_block.
    def visitFilter_block(self, ctx:ReportDSLParser.Filter_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#filter_expression.
    def visitFilter_expression(self, ctx:ReportDSLParser.Filter_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#aggregate_def.
    def visitAggregate_def(self, ctx:ReportDSLParser.Aggregate_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#calculate_def.
    def visitCalculate_def(self, ctx:ReportDSLParser.Calculate_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#calculation_expression.
    def visitCalculation_expression(self, ctx:ReportDSLParser.Calculation_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#layout_block.
    def visitLayout_block(self, ctx:ReportDSLParser.Layout_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ReportDSLParser#layout_param.
    def visitLayout_param(self, ctx:ReportDSLParser.Layout_paramContext):
        return self.visitChildren(ctx)



del ReportDSLParser