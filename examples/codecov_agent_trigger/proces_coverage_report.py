#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
from typing import Any

from codegen import Agent

from generate_codecov_agent_prompt import generate_codecov_agent_prompt

ORG_ID = 1

def parse_coverage_xml(xml_file: str) -> dict[str, Any]:
    """Parse the coverage.xml file and extract relevant information.

    Args:
        xml_file: Path to the coverage XML file.

    Returns:
        Dictionary containing parsed coverage data.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Extract overall coverage statistics
        coverage_data = {
            "version": root.get("version"),
            "timestamp": root.get("timestamp"),
            "lines_covered": int(root.get("lines-covered", 0)),
            "lines_valid": int(root.get("lines-valid", 0)),
            "line_rate": float(root.get("line-rate", 0)),
            "branches_covered": int(root.get("branches-covered", 0)),
            "branches_valid": int(root.get("branches-valid", 0)),
            "branch_rate": float(root.get("branch-rate", 0)),
            "complexity": float(root.get("complexity", 0)),
        }

        # Calculate overall coverage percentage
        if coverage_data["lines_valid"] > 0:
            coverage_data["coverage_percentage"] = coverage_data["lines_covered"] / coverage_data["lines_valid"] * 100
        else:
            coverage_data["coverage_percentage"] = 0

        return coverage_data

    except Exception as e:
        print(f"Error parsing coverage XML: {e}")
        return {}


def main():
    """Main function to process the coverage report."""
    if len(sys.argv) < 5:
        print("Usage: python process_coverage_report.py <coverage_xml_file> <pr_number> <repo> <token>")
        sys.exit(1)

    xml_file = sys.argv[1]
    pr_number = sys.argv[2]
    repo = sys.argv[3]
    token = sys.argv[4]

    coverage_data = parse_coverage_xml(xml_file)
    coverage_data["pr_number"] = pr_number
    coverage_data["repo"] = repo
    coverage_data["token"] = token

    if not coverage_data:
        print("Failed to parse coverage data")
        sys.exit(1)

    # Example: Check if coverage meets a threshold
    threshold = 77  # 77% coverage threshold
    if coverage_data["coverage_percentage"] < threshold:
        print(f"\nWARNING: Coverage {coverage_data['coverage_percentage']:.2f}% is below threshold of {threshold}%")
        print("Agent will be notified.")
        new_agent = Agent(token=token, org_id=ORG_ID)
        second_task = new_agent.run(generate_codecov_agent_prompt(pr_number, repo))
        print(f"Agent has been notified. URL: {second_task.web_url}")
    else:
        print("Coverage is above threshold.")


if __name__ == "__main__":
    main()
