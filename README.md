# Numou Security

Security is an independently versioned capability repository built on the Numou Core Platform.

## Ownership
- Authentication: credential verification, password hashing and upgrade, MFA, sessions and federation security.
- Authorization: contextual RBAC/ABAC, permission and policy evaluation, resource/action decisions and enforcement contracts.
- Security audit: authentication, credential lifecycle and policy-decision security records.
- Vault: secret lifecycle, encrypted secret storage, cryptographic envelope operations and PostgreSQL persistence.
- Security adapters: Quarkus request/security filters and the optional Social Graph authorization bridge.

Identity owns canonical principals and profile records. Core (`numu`) owns tenant lifecycle and tenant context. Tenant membership is not an implicit role grant. Business audit facts remain owned by their business capabilities.

## Build prerequisites
- Java 21.
- Published `tech.kayys.numou:numou-parent:0.1.0-SNAPSHOT` and Core platform BOM `tech.kayys.numou:numou-bom:0.1.0-SNAPSHOT`.
- Core Foundation, Cache, Observability and Social Graph artifacts required by selected adapters.
- GitHub Packages read access to `andalus-ai/numu` and write access to this repository's package endpoint.

Configure credentials using environment-backed Maven settings; never commit tokens.

## Build
```bash
mvn -B -ntp verify
```

A clean independent build is not accepted until the parent, Core BOM and all required Core artifacts resolve from GitHub Packages in a clean environment.

## Scope notes
The source contains two legacy vault POM roots, `vault-secret/` and `vault-secret-cloud/`, which are not declared in the active `security/pom.xml` reactor. They are intentionally excluded until their status and intended ownership are reviewed. The `social-graph-adapter` is included only as an integration adapter; Social Graph domain ownership remains in Core.

## Source provenance
Extracted from andalus-ai/numu/security/ at source commit 9bd74574796486a3b86312b28f589e30de347885. Ten active modules and tests/resources retained. Root aggregator and BOM rebuilt; legacy source BOM was incorrectly named numou-bom and included unrelated artifacts. Original monorepo remains authoritative until clean builds, consumer migration and release acceptance pass.