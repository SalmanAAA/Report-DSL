# Generated from ReportDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ReportDSLParser import ReportDSLParser
else:
    from ReportDSLParser import ReportDSLParser

# This class defines a complete listener for a parse tree produced by ReportDSLParser.
class ReportDSLListener(ParseTreeListener):

    # Enter a parse tree produced by ReportDSLParser#report_definition.
    def enterReport_definition(self, ctx:ReportDSLParser.Report_definitionContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#report_definition.
    def exitReport_definition(self, ctx:ReportDSLParser.Report_definitionContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#report_header.
    def enterReport_header(self, ctx:ReportDSLParser.Report_headerContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#report_header.
    def exitReport_header(self, ctx:ReportDSLParser.Report_headerContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#data_source_block.
    def enterData_source_block(self, ctx:ReportDSLParser.Data_source_blockContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#data_source_block.
    def exitData_source_block(self, ctx:ReportDSLParser.Data_source_blockContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#filter_block.
    def enterFilter_block(self, ctx:ReportDSLParser.Filter_blockContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#filter_block.
    def exitFilter_block(self, ctx:ReportDSLParser.Filter_blockContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#filter_expression.
    def enterFilter_expression(self, ctx:ReportDSLParser.Filter_expressionContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#filter_expression.
    def exitFilter_expression(self, ctx:ReportDSLParser.Filter_expressionContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#aggregate_def.
    def enterAggregate_def(self, ctx:ReportDSLParser.Aggregate_defContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#aggregate_def.
    def exitAggregate_def(self, ctx:ReportDSLParser.Aggregate_defContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#calculate_def.
    def enterCalculate_def(self, ctx:ReportDSLParser.Calculate_defContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#calculate_def.
    def exitCalculate_def(self, ctx:ReportDSLParser.Calculate_defContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#calculation_expression.
    def enterCalculation_expression(self, ctx:ReportDSLParser.Calculation_expressionContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#calculation_expression.
    def exitCalculation_expression(self, ctx:ReportDSLParser.Calculation_expressionContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#layout_block.
    def enterLayout_block(self, ctx:ReportDSLParser.Layout_blockContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#layout_block.
    def exitLayout_block(self, ctx:ReportDSLParser.Layout_blockContext):
        pass


    # Enter a parse tree produced by ReportDSLParser#layout_param.
    def enterLayout_param(self, ctx:ReportDSLParser.Layout_paramContext):
        pass

    # Exit a parse tree produced by ReportDSLParser#layout_param.
    def exitLayout_param(self, ctx:ReportDSLParser.Layout_paramContext):
        pass



del ReportDSLParser