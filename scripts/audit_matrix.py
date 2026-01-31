#!/usr/bin/env python3
"""
AURORA Trading System - Audit Matrix Report Generator
Generates comprehensive audit reports in JSON, YAML, and CSV formats
Version: 1.0
Author: Tech Lead
Date: 2026-01-31
"""

import json
import yaml
import csv
import os
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class AuditFile:
    """Represents an audited file"""
    file_id: int
    name: str
    path: str
    file_type: str
    module: str
    status: str


@dataclass
class CriticalGap:
    """Represents a critical gap in the project"""
    gap_id: int
    title: str
    severity: str
    impact: str
    effort_hours: int
    timeline_week: str


@dataclass
class ProjectPhase:
    """Represents a project phase"""
    phase_id: int
    name: str
    timeline: str
    files_count: int
    effort_hours: int
    status: str
    blockers: str


class AuditMatrixGenerator:
    """Generate audit reports with multiple output formats"""

    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = output_dir
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.existing_files: List[AuditFile] = []
        self.critical_gaps: List[CriticalGap] = []
        self.project_phases: List[ProjectPhase] = []

    def add_file(self, audit_file: AuditFile) -> None:
        """Add a file to audit"""
        self.existing_files.append(audit_file)

    def add_gap(self, gap: CriticalGap) -> None:
        """Add a critical gap"""
        self.critical_gaps.append(gap)

    def add_phase(self, phase: ProjectPhase) -> None:
        """Add a project phase"""
        self.project_phases.append(phase)

    def generate_json_report(self) -> str:
        """Generate JSON format report"""
        report = {
            "audit_metadata": {
                "timestamp": self.timestamp,
                "total_existing_files": len(self.existing_files),
                "total_critical_gaps": len(self.critical_gaps),
                "total_phases": len(self.project_phases),
                "coverage": f"{(len(self.existing_files) / 57) * 100:.1f}%"
            },
            "existing_files": [asdict(f) for f in self.existing_files],
            "critical_gaps": [asdict(g) for g in self.critical_gaps],
            "project_phases": [asdict(p) for p in self.project_phases]
        }
        return json.dumps(report, indent=2)

    def generate_yaml_report(self) -> str:
        """Generate YAML format report"""
        report = {
            "audit_metadata": {
                "timestamp": self.timestamp,
                "total_existing_files": len(self.existing_files),
                "total_critical_gaps": len(self.critical_gaps),
                "total_phases": len(self.project_phases),
                "coverage": f"{(len(self.existing_files) / 57) * 100:.1f}%"
            },
            "existing_files": [asdict(f) for f in self.existing_files],
            "critical_gaps": [asdict(g) for g in self.critical_gaps],
            "project_phases": [asdict(p) for p in self.project_phases]
        }
        return yaml.dump(report, default_flow_style=False)

    def generate_csv_report(self) -> str:
        """Generate CSV format report"""
        output = []
        output.append("EXISTING FILES AUDIT\n")
        output.append("file_id,name,path,type,module,status\n")
        
        for f in self.existing_files:
            output.append(f"{f.file_id},{f.name},{f.path},{f.file_type},{f.module},{f.status}\n")
        
        output.append("\n\nCRITICAL GAPS ANALYSIS\n")
        output.append("gap_id,title,severity,impact,effort_hours,timeline_week\n")
        
        for g in self.critical_gaps:
            output.append(f"{g.gap_id},{g.title},{g.severity},{g.impact},{g.effort_hours},{g.timeline_week}\n")
        
        output.append("\n\nPROJECT PHASES\n")
        output.append("phase_id,name,timeline,files_count,effort_hours,status,blockers\n")
        
        for p in self.project_phases:
            output.append(f"{p.phase_id},{p.name},{p.timeline},{p.files_count},{p.effort_hours},{p.status},{p.blockers}\n")
        
        return "".join(output)

    def save_reports(self) -> None:
        """Save all report formats to files"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save JSON
        json_report = self.generate_json_report()
        with open(os.path.join(self.output_dir, "audit_report.json"), "w") as f:
            f.write(json_report)
        print(f"✅ JSON report saved: {os.path.join(self.output_dir, 'audit_report.json')}")
        
        # Save YAML
        yaml_report = self.generate_yaml_report()
        with open(os.path.join(self.output_dir, "audit_report.yaml"), "w") as f:
            f.write(yaml_report)
        print(f"✅ YAML report saved: {os.path.join(self.output_dir, 'audit_report.yaml')}")
        
        # Save CSV
        csv_report = self.generate_csv_report()
        with open(os.path.join(self.output_dir, "audit_report.csv"), "w") as f:
            f.write(csv_report)
        print(f"✅ CSV report saved: {os.path.join(self.output_dir, 'audit_report.csv')}")

    def print_summary(self) -> None:
        """Print audit summary to console"""
        print("\n" + "="*60)
        print("AURORA TRADING SYSTEM - AUDIT MATRIX REPORT")
        print("="*60)
        print(f"Timestamp: {self.timestamp}")
        print(f"Existing Files: {len(self.existing_files)}")
        print(f"Critical Gaps: {len(self.critical_gaps)}")
        print(f"Project Phases: {len(self.project_phases)}")
        coverage = (len(self.existing_files) / 57) * 100
        print(f"Coverage: {coverage:.1f}%")
        print(f"Total Effort: 234 hours")
        print(f"Timeline: 4 weeks")
        print("="*60 + "\n")


def main():
    """Main execution"""
    print("🚀 AURORA Audit Matrix Report Generator v1.0\n")
    
    # Initialize generator
    generator = AuditMatrixGenerator(output_dir="./reports")
    
    # Add existing files (13 REAL FILES)
    existing_files_data = [
        (1, "02-KPI_DASHBOARD_SPEC_v1.0.md", "00-Governance/SPECIFICATIONS/", "md", "GOVERNANCE", "complete"),
        (2, "requirements.txt", "./", "txt", "CONFIG", "complete"),
        (3, "setup-venv.ps1", "./", "ps1", "DEPLOYMENT", "complete"),
        (4, "setup-aurora-local.ps1", "./", "ps1", "DEPLOYMENT", "complete"),
        (5, ".env.example", "./", "txt", "CONFIG", "complete"),
        (6, "README.md", "./", "md", "DOCS", "partial"),
        (7, "LICENSE", "./", "txt", "GOVERNANCE", "complete"),
        (8, ".gitignore", "./", "txt", "CONFIG", "complete"),
        (9, "settings.json", ".vscode/", "json", "CONFIG", "complete"),
        (10, "extensions.json", ".vscode/", "json", "CONFIG", "complete"),
        (11, "audit_report.json", "./", "json", "GOVERNANCE", "complete"),
        (12, "audit_report.yaml", "./", "yaml", "GOVERNANCE", "complete"),
        (13, "audit_matrix.py", "scripts/", "py", "GOVERNANCE", "complete"),
    ]
    
    for file_data in existing_files_data:
        audit_file = AuditFile(*file_data)
        generator.add_file(audit_file)
    
    # Add critical gaps (12 REAL GAPS)
    gaps_data = [
        (1, "Sistema de Configuração Centralizado", "Critical", "Sem gerenciamento de variáveis", 4, "1"),
        (2, "Camada de Banco de Dados", "Critical", "Sem persistência de dados", 12, "1-2"),
        (3, "Engine de Trading", "Critical", "Sem funcionalidade principal", 24, "2-3"),
        (4, "Validação de Segurança", "Critical", "Sistema exposto a riscos", 16, "2"),
        (5, "API REST", "Critical", "Sem endpoints para cliente", 20, "3"),
        (6, "Prometheus Metrics", "Critical", "Sem observabilidade", 12, "2"),
        (7, "Expert Advisor MQL5", "Critical", "Sem automação de trading", 30, "3-4"),
        (8, "Sistema de Testes", "High", "Sem garantia de qualidade", 40, "2-4"),
        (9, "Documentação Técnica", "High", "Dificuldade de onboarding", 20, "4"),
        (10, "CI/CD Pipeline", "High", "Sem automação de deploy", 16, "4"),
        (11, "Docker & Deployment", "High", "Sem containerização", 24, "4-5"),
        (12, "Notificações e Alertas", "High", "Sem comunicação de eventos", 12, "3"),
    ]
    
    for gap_data in gaps_data:
        gap = CriticalGap(*gap_data)
        generator.add_gap(gap)
    
    # Add project phases (4 REAL PHASES)
    phases_data = [
        (1, "CORE SYSTEM", "Week 1-2", 12, 32, "pending", "None"),
        (2, "MODULES", "Week 2-3", 16, 68, "pending", "Phase 1 complete"),
        (3, "SCHEMAS & MQL5", "Week 3-4", 10, 74, "pending", "Phase 2 partial"),
        (4, "DOCUMENTATION & DEPLOYMENT", "Week 4", 6, 60, "pending", "Phase 1-3 complete"),
    ]
    
    for phase_data in phases_data:
        phase = ProjectPhase(*phase_data)
        generator.add_phase(phase)
    
    # Generate and save reports
    generator.save_reports()
    generator.print_summary()
    
    print("✅ Audit reports generated successfully!")
    print(f"📁 Reports location: {os.path.abspath(generator.output_dir)}\n")


if __name__ == "__main__":
    main()
