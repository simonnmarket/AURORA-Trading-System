from dataclasses import dataclass
import json
import yaml
import csv
from typing import List

@dataclass
class AuditFile:
    name: str
    timestamp: str

@dataclass
class CriticalGap:
    start: str
    end: str
    reason: str

class AuditMatrixGenerator:
    def __init__(self):
        self.audit_files: List[AuditFile] = []
        self.critical_gaps: List[CriticalGap] = []

    def add_audit_file(self, name: str, timestamp: str):
        self.audit_files.append(AuditFile(name, timestamp))

    def add_critical_gap(self, start: str, end: str, reason: str):
        self.critical_gaps.append(CriticalGap(start, end, reason))

    def save_reports(self, filename: str):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Audit File', 'Timestamp'])
            for audit in self.audit_files:
                writer.writerow([audit.name, audit.timestamp])

    def print_summary(self):
        print(f'Number of audit files: {len(self.audit_files)}')
        print(f'Number of critical gaps: {len(self.critical_gaps)}')

# Example usage
if __name__ == '__main__':
    generator = AuditMatrixGenerator()
    generator.add_audit_file('audit_2026-01-31.json', '2026-01-31T22:21:08Z')
    generator.add_critical_gap('2026-01-31T22:21:00Z', '2026-01-31T22:21:05Z', 'Network delay')
    generator.save_reports('audit_report.csv')
    generator.print_summary()
