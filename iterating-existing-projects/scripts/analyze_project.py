#!/usr/bin/env python3
"""
Project Structure Analyzer
Analyzes existing project to identify patterns and conventions
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

class ProjectAnalyzer:
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.results = {
            "structure": {},
            "patterns": {},
            "conventions": {},
            "dependencies": {},
            "recommendations": []
        }

    def analyze(self) -> Dict:
        """Run complete project analysis"""
        print("🔍 Starting project analysis...")

        self.analyze_structure()
        self.detect_architecture_pattern()
        self.analyze_naming_conventions()
        self.analyze_dependencies()
        self.check_for_ai_instructions()
        self.generate_recommendations()

        return self.results

    def analyze_structure(self):
        """Analyze directory structure"""
        structure = defaultdict(list)

        # Common directories to look for
        important_dirs = {
            'src', 'lib', 'app', 'components', 'views', 'models',
            'controllers', 'services', 'utils', 'helpers', 'tests',
            'spec', 'features', 'domain', 'infrastructure', 'api',
            'routes', 'middleware', 'public', 'static', 'assets'
        }

        for root, dirs, files in os.walk(self.root):
            # Skip hidden and build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'dist', 'build']]

            level = root.replace(str(self.root), '').count(os.sep)
            if level < 4:  # Only analyze up to 4 levels deep
                path = Path(root)
                rel_path = path.relative_to(self.root)

                for dir_name in dirs:
                    if dir_name.lower() in important_dirs:
                        structure[str(rel_path)].append(dir_name)

        self.results["structure"]["directories"] = dict(structure)

    def detect_architecture_pattern(self):
        """Detect common architectural patterns"""
        patterns = []
        dirs = set()

        for root, dir_list, _ in os.walk(self.root):
            for d in dir_list:
                dirs.add(d.lower())

        # Pattern detection rules
        if {'models', 'views', 'controllers'} <= dirs:
            patterns.append("MVC")

        if {'domain', 'application', 'infrastructure'} <= dirs:
            patterns.append("Clean Architecture")

        if {'components', 'containers'} <= dirs:
            patterns.append("Component-Based (React/Vue style)")

        if {'modules'} <= dirs:
            patterns.append("Module-Based")

        if {'src', 'tests'} <= dirs or {'src', 'spec'} <= dirs:
            patterns.append("Standard src/test separation")

        self.results["patterns"]["architecture"] = patterns

    def analyze_naming_conventions(self):
        """Analyze file and variable naming conventions"""
        file_patterns = Counter()

        # Analyze file naming
        for root, _, files in os.walk(self.root):
            for file in files:
                if file.endswith(('.js', '.ts', '.py', '.jsx', '.tsx', '.vue')):
                    if re.match(r'^[A-Z]', file):
                        file_patterns['PascalCase'] += 1
                    elif re.match(r'^[a-z]+(?:[A-Z][a-z]+)*', file):
                        file_patterns['camelCase'] += 1
                    elif '_' in file:
                        file_patterns['snake_case'] += 1
                    elif '-' in file:
                        file_patterns['kebab-case'] += 1

        # Determine dominant pattern
        if file_patterns:
            dominant = max(file_patterns, key=file_patterns.get)
            self.results["conventions"]["file_naming"] = {
                "dominant": dominant,
                "distribution": dict(file_patterns)
            }

    def analyze_dependencies(self):
        """Analyze project dependencies"""
        deps = {}

        # Check for package.json (Node.js)
        package_json = self.root / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                deps["javascript"] = {
                    "dependencies": list(data.get("dependencies", {}).keys()),
                    "devDependencies": list(data.get("devDependencies", {}).keys()),
                    "package_manager": self.detect_package_manager()
                }

        # Check for requirements.txt or pyproject.toml (Python)
        requirements_txt = self.root / "requirements.txt"
        pyproject_toml = self.root / "pyproject.toml"

        if requirements_txt.exists():
            with open(requirements_txt) as f:
                deps["python"] = {
                    "dependencies": [line.strip() for line in f if line.strip() and not line.startswith('#')],
                    "package_manager": "pip"
                }
        elif pyproject_toml.exists():
            deps["python"] = {
                "config_file": "pyproject.toml",
                "package_manager": "poetry/pip"
            }

        # Check for go.mod (Go)
        go_mod = self.root / "go.mod"
        if go_mod.exists():
            deps["go"] = {"config_file": "go.mod"}

        self.results["dependencies"] = deps

    def detect_package_manager(self) -> str:
        """Detect which package manager is being used"""
        if (self.root / "yarn.lock").exists():
            return "yarn"
        elif (self.root / "pnpm-lock.yaml").exists():
            return "pnpm"
        elif (self.root / "package-lock.json").exists():
            return "npm"
        return "unknown"

    def check_for_ai_instructions(self):
        """Check for AI-specific instruction files"""
        ai_files = []

        patterns = [
            "CLAUDE.md", "AI.md", "INSTRUCTIONS.md", ".claude",
            "COPILOT.md", "ASSISTANT.md", "CONTEXT.md"
        ]

        for pattern in patterns:
            matches = list(self.root.rglob(pattern))
            for match in matches:
                ai_files.append(str(match.relative_to(self.root)))

        if ai_files:
            self.results["patterns"]["ai_instructions"] = ai_files
            self.results["recommendations"].append(
                "Found AI instruction files - READ THESE FIRST before making modifications"
            )

    def generate_recommendations(self):
        """Generate recommendations based on analysis"""
        recs = self.results["recommendations"]

        # Architecture recommendations
        if self.results["patterns"].get("architecture"):
            arch = self.results["patterns"]["architecture"][0]
            recs.append(f"Project follows {arch} pattern - maintain this structure")

        # Naming convention recommendations
        if self.results["conventions"].get("file_naming"):
            naming = self.results["conventions"]["file_naming"]["dominant"]
            recs.append(f"Use {naming} for new files to match existing convention")

        # Dependency recommendations
        if self.results["dependencies"].get("javascript"):
            pm = self.results["dependencies"]["javascript"]["package_manager"]
            if pm != "unknown":
                recs.append(f"Use {pm} for package management")

        # Test framework detection
        if self.results["dependencies"].get("javascript"):
            deps = self.results["dependencies"]["javascript"].get("devDependencies", [])
            if "jest" in deps:
                recs.append("Use Jest for testing")
            elif "mocha" in deps:
                recs.append("Use Mocha for testing")
            elif "vitest" in deps:
                recs.append("Use Vitest for testing")

def main():
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    analyzer = ProjectAnalyzer(path)
    results = analyzer.analyze()

    # Print results
    print("\n" + "="*50)
    print("📊 PROJECT ANALYSIS RESULTS")
    print("="*50)

    # Architecture
    if results["patterns"].get("architecture"):
        print("\n🏗️  Architecture Pattern:")
        for pattern in results["patterns"]["architecture"]:
            print(f"  • {pattern}")

    # AI Instructions
    if results["patterns"].get("ai_instructions"):
        print("\n🤖 AI Instruction Files Found:")
        for file in results["patterns"]["ai_instructions"]:
            print(f"  • {file}")

    # Naming Conventions
    if results["conventions"].get("file_naming"):
        naming = results["conventions"]["file_naming"]
        print(f"\n📝 File Naming Convention: {naming['dominant']}")

    # Dependencies
    if results["dependencies"]:
        print("\n📦 Dependencies:")
        for lang, info in results["dependencies"].items():
            print(f"  {lang.capitalize()}:")
            if "package_manager" in info:
                print(f"    Package Manager: {info['package_manager']}")
            if "dependencies" in info:
                print(f"    Dependencies: {len(info['dependencies'])} packages")

    # Recommendations
    if results["recommendations"]:
        print("\n💡 Recommendations:")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"  {i}. {rec}")

    # Save detailed results
    output_file = Path("project_analysis.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n📁 Detailed results saved to: {output_file}")

if __name__ == "__main__":
    main()