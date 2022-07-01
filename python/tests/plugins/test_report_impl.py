from unittest import TestCase

from aac.plugins.plugin_execution import PluginExecutionStatusCode
from aac.plugins.report.report_impl import report, report_csv


class TestReport(TestCase):
    def test_report(self):
        # TODO: Write tests for report

        report_definition_file = str()
        architecture_file = str()
        --output_file = str()
        
        result = report(report_definition_file=report_definition_file, architecture_file=architecture_file, --output_file=--output_file)
        self.assertEqual(result.status_code, PluginExecutionStatusCode.SUCCESS)
    
    def test_report_csv(self):
        # TODO: Write tests for report_csv

        report_definition_file = str()
        architecture_file = str()
        --output_file = str()
        
        result = report_csv(report_definition_file=report_definition_file, architecture_file=architecture_file, --output_file=--output_file)
        self.assertEqual(result.status_code, PluginExecutionStatusCode.SUCCESS)
    
