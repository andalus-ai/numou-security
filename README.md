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
