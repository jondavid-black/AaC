from unittest import TestCase

from tempfile import TemporaryDirectory
from tests.helpers.io import temporary_test_file
from tests.helpers.plugins import YAML_FILE_EXTENSION

from aac.plugins.plugin_execution import PluginExecutionStatusCode
from aac.plugins.report.report_impl import report, report_csv

TEST_SIMPLE_REPORT_YAML = f"""
report:
  name: Parts List
  description: A list of all parts for the apartment.
  data:
    - name: Part Make
      description: The vendor of the part.
      source: part.make
    - name: Part Model
      description: The manufacturer model identifier.
      source: part.model
    - name: Part Unit Cost
      description: What the part costs.
      source: part.unit_cost
    - name: Part Description
      description: The manufacturer description of the part.
      source: part.description
"""

TEST_SIMPLE_ARCH_PART_YAML = f"""
part:
  name: Coasters
  make: HUAOAO
  model: Cork Coaster Set
  description: Set of 12 plain cork coasters.
  unit_cost: 7.19
  quote_type: Web_Reference
  quote: https://smile.amazon.com/Coaster-Absorbent-Resistant-Reusable-Coasters/dp/B08PZ15J2N
---
part:
  name: TV
  make: Samsung
  model: S-Z452-OG2331-55-HD
  description: 55 inch high-definition smart tv
  unit_cost: 682.23
  quote_type: Web_Reference
  quote: https://www.google.com
---
part:
  name: Wifi_Router
  make: NetGear
  model: N334521939
  description: 802.11 a/b/g
  unit_cost: 88.33
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: Sound_Bar
  make: Loudness Inc
  model: LI-35-ST-HDMI-BT-334
  description: Something better than the built-in tv speakers
  unit_cost: 120.23
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: X_Box
  make: Microsoft
  model: X-Box One v2
  description: Streaming and gaming device
  unit_cost: 599.99
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: Coffee_Pot
  make: Perky Mornings
  model: Dual-brew 2200
  description: Coffee maker with drip and k-cup
  unit_cost: 199.99
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: Blender
  make: Grind House
  model: Liquificationinator 1000
  description: 7 setting industrial strength blender with pulse
  unit_cost: 99.99
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: Pans
  make: Affordable Living
  model: 12-al-33288
  description: 12 piece aluminum pots and pans
  unit_cost: 299.99
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: Dishes
  make: Affordable Living
  model: 2251-AHRSU-8
  description: 8 place setting dinner ware set
  unit_cost: 129.99
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: Utensils
  make: Affordable Living
  model: XG-33445
  description: Complete set of knives, spatulas, measuring cups, and whisks
  unit_cost: 99.99
  quote_type: Web_Reference
  quote: https://smile.amazon.com
---
part:
  name: Silverware
  make: Affordable Living
  model: 8835-AHTTR-12
  description: 12 settings of fork, spoon, and butter knife
  unit_cost: 139.99
  quote_type: Web_Reference
  quote: https://smile.amazon.com
"""

class TestReport(TestCase):
    def test_simple_report(self):
        with TemporaryDirectory() as temp_directory, temporary_test_file(TEST_SIMPLE_REPORT_YAML, dir=temp_directory, suffix=YAML_FILE_EXTENSION) as report_yaml, temporary_test_file(TEST_SIMPLE_ARCH_PART_YAML, dir=temp_directory, suffix=YAML_FILE_EXTENSION) as arch_yaml:

            result = report(report_yaml.name, arch_yaml.name)
            print(f"messages = {result.messages}")
        self.assertEqual(result.status_code, PluginExecutionStatusCode.SUCCESS)

    def test_simple_report_csv(self):
        # TODO: Write tests for report_csv
        with TemporaryDirectory() as temp_directory, temporary_test_file(TEST_SIMPLE_REPORT_YAML, dir=temp_directory, suffix=YAML_FILE_EXTENSION) as report_yaml, temporary_test_file(TEST_SIMPLE_ARCH_PART_YAML, dir=temp_directory, suffix=YAML_FILE_EXTENSION) as arch_yaml:

            result = report_csv(report_yaml.name, arch_yaml.name)
            print(f"messages = {result.messages}")
        self.assertEqual(result.status_code, PluginExecutionStatusCode.SUCCESS)