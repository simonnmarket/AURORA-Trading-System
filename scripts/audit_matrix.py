import json
import os
import sys

class AuditMatrix:
    def __init__(self, report_file):
        self.report_file = report_file

    def generate_audit_report(self, data):
        # Generate and save audit report
        with open(self.report_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Audit report generated: {self.report_file}")

    def parse_audit_report(self):
        # Load and parse audit report
        if not os.path.exists(self.report_file):
            print(f"Error: {self.report_file} does not exist.")
            return
        with open(self.report_file, 'r') as f:
            data = json.load(f)
            return data

# Example usage
if __name__ == '__main__':
    audit = AuditMatrix('audit_report.json') 
    audit_data = {'timestamp': '2026-01-31 22:07:17', 'info': 'Sample audit information'}
    audit.generate_audit_report(audit_data)
    parsed_data = audit.parse_audit_report()
    print(parsed_data)