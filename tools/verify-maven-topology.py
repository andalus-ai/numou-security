#!/usr/bin/env python3
"""Validate the standalone Numou Security Maven reactor and BOM contracts."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

NS = {"m": "http://maven.apache.org/POM/4.0.0"}
ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "security-domain": "numou-security-domain",
    "security-spi": "numou-security-spi",
    "security-application": "numou-security-application",
    "security-adapter": "numou-security-adapter",
    "social-graph-adapter": "numou-security-social-graph-adapter",
    "security-vault-domain": "numou-security-vault-domain",
    "security-vault-spi": "numou-security-vault-spi",
    "security-vault-application": "numou-security-vault-application",
    "security-vault-postgres": "numou-security-vault-postgres",
    "security-vault-crypto": "numou-security-vault-crypto",
    "vault-secret": "numou-security-vault-secret",
    "vault-secret-cloud": "numou-security-vault-secret-cloud",
}
EXPECTED_MODULES = ["bom", *EXPECTED.keys()]


def parse(path: Path) -> ET.Element:
    if not path.is_file():
        raise AssertionError(f"Missing POM: {path.relative_to(ROOT)}")
    return ET.parse(path).getroot()


def value(node: ET.Element, path: str) -> str | None:
    found = node.find(path, NS)
    return found.text.strip() if found is not None and found.text else None


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


try:
    root = parse(ROOT / "pom.xml")
    if value(root, "m:artifactId") != "numou-security":
        fail("root artifactId must be numou-security")
    if value(root, "m:parent/m:artifactId") != "numou-parent":
        fail("root must inherit the neutral numou-parent")
    if value(root, "m:parent/m:relativePath") not in ("", None):
        fail("root parent relativePath must be empty")

    modules = [n.text.strip() for n in root.findall("m:modules/m:module", NS)]
    if modules != EXPECTED_MODULES:
        fail(f"root modules mismatch: expected {EXPECTED_MODULES}, got {modules}")

    root_imports = {
        value(d, "m:artifactId")
        for d in root.findall("m:dependencyManagement/m:dependencies/m:dependency", NS)
        if value(d, "m:type") == "pom" and value(d, "m:scope") == "import"
    }
    if "numou-bom" not in root_imports:
        fail("root must import the shared numou-bom")

    internal_artifacts = set(EXPECTED.values())
    for module, artifact in EXPECTED.items():
        pom = parse(ROOT / module / "pom.xml")
        if value(pom, "m:artifactId") != artifact:
            fail(f"{module}/pom.xml has wrong artifactId")
        if value(pom, "m:parent/m:artifactId") != "numou-security":
            fail(f"{module}/pom.xml must inherit numou-security")
        if value(pom, "m:parent/m:groupId") != "tech.kayys.numou":
            fail(f"{module}/pom.xml has wrong parent groupId")
        for dep in pom.findall("m:dependencies/m:dependency", NS):
            dep_artifact = value(dep, "m:artifactId")
            if dep_artifact in internal_artifacts and value(dep, "m:version") != "${project.version}":
                fail(f"{module} must version internal dependency {dep_artifact} with project.version")

    bom = parse(ROOT / "bom/pom.xml")
    if value(bom, "m:artifactId") != "numou-security-bom":
        fail("BOM artifactId must be numou-security-bom")
    if value(bom, "m:parent/m:artifactId") != "numou-parent":
        fail("BOM must inherit neutral numou-parent")
    managed = {
        value(d, "m:artifactId")
        for d in bom.findall("m:dependencyManagement/m:dependencies/m:dependency", NS)
        if value(d, "m:type") != "pom" or value(d, "m:scope") != "import"
    }
    if managed != internal_artifacts:
        fail(f"Security BOM managed artifacts mismatch: missing={sorted(internal_artifacts-managed)}, extra={sorted(managed-internal_artifacts)}")
    bom_imports = [
        value(d, "m:artifactId")
        for d in bom.findall("m:dependencyManagement/m:dependencies/m:dependency", NS)
        if value(d, "m:type") == "pom" and value(d, "m:scope") == "import"
    ]
    if "numou-bom" not in bom_imports:
        fail("Security BOM must import shared numou-bom")
    target = value(bom, "m:distributionManagement/m:repository/m:url")
    if target != "https://maven.pkg.github.com/andalus-ai/numou-security":
        fail("Security BOM must publish to the numou-security GitHub Packages repository")

    print(f"Security Maven topology passed: {len(EXPECTED)} capability modules and {len(internal_artifacts)} BOM-managed artifacts.")
except (ET.ParseError, AssertionError) as exc:
    fail(str(exc))
