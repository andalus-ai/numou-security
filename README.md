# Numou Security

Security is a reusable capability repository in the Numou platform.

## Scope

- Contextual authorization contracts and policy evaluation
- Authentication and request-security adapters
- Append-only security audit contracts and adapters
- Vault domain, SPI, application and persistence/cryptographic adapters
- Secret-management modules, including cloud integration
- Social Graph integration adapter only; Social Graph domain ownership remains in Numou Core

## Ownership boundaries

- Core (andalus-ai/numu) owns Foundation, tenant lifecycle/context, runtime and shared platform contracts.
- Identity (numou-identity) owns users, principals, credentials and organization identity.
- Security (this repository) owns authentication/authorization policy services, security audit, vault and secret-management behavior.
- Tenant membership is not an application role. Authorization must evaluate the authenticated subject, verified tenant context, resource, action and relevant policy context.
- This repository consumes Core and Identity contracts; Core must never depend on this repository.

## Maven

Parent: tech.kayys.numou:numou-parent:0.1.0-SNAPSHOT
Shared platform BOM: tech.kayys.numou:numou-bom:0.1.0-SNAPSHOT
Capability BOM: tech.kayys.numou:numou-security-bom:0.1.0-SNAPSHOT
Source package repository: https://maven.pkg.github.com/andalus-ai/numu
Publication target: https://maven.pkg.github.com/andalus-ai/numou-security

Configure Maven settings so the neutral parent can be resolved before the project POM is read. Add a server and an active repository profile (substitute a suitable username and inject the token through an environment variable):

```xml
<settings>
  <servers>
    <server>
      <id>github</id>
      <username>${env.GITHUB_ACTOR}</username>
      <password>${env.GITHUB_TOKEN}</password>
    </server>
  </servers>
  <profiles>
    <profile>
      <id>numou-packages</id>
      <repositories>
        <repository>
          <id>github</id>
          <url>https://maven.pkg.github.com/andalus-ai/numu</url>
        </repository>
      </repositories>
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>numou-packages</activeProfile>
  </activeProfiles>
</settings>
```

The token needs package read access to the Core repository and package write access to this repository for publication. Never commit credentials.

## Build

mvn -B -ntp verify

A clean independent build is not claimed by the source-transfer commit. It requires the neutral parent, shared platform BOM and all consumed Core artifacts to be published and accessible. CI should verify the full reactor with a clean local Maven repository before release.

## Source provenance

The source files in this repository are transferred from andalus-ai/numu/security/ at source commit 9bd74574796486a3b86312b28f589e30de347885. The transfer preserves 172 source files while replacing the monorepo root POM and legacy shared BOM with repository-specific Maven metadata. The source monorepo remains authoritative until this repository has passed clean build, security tests, package publication and consumer migration gates. Do not delete or disable the source modules as part of this extraction PR.
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
