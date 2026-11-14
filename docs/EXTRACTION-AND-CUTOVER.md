# Security Extraction and Cutover Plan

## Status

- Source modules are staged in this repository on `m1/extract-security-and-vault`.
- The source of truth remains `andalus-ai/numu/security/` until this extraction is accepted and all consumers are migrated.
- The PR's structural reactor/BOM check passes.
- The remote Maven verification is deliberately opt-in because the shared Core parent/BOM and Core artifacts must first be published and readable from GitHub Packages.
- Do not delete or disable the monorepo modules as part of this staging PR.

## Module inventory

| Module | Responsibility |
| --- | --- |
| `security-domain` | Principal/permission/access-decision model, authentication results and security audit domain |
| `security-spi` | Authentication, policy and audit infrastructure ports |
| `security-application` | Authorization, tenant-aware security context, rate limiting and redaction services |
| `security-adapter` | Quarkus request filters, OIDC integration, security headers and safe problem responses |
| `social-graph-adapter` | Optional bridge from verified security context to Social Graph authorization |
| `security-vault-domain` | Secret and vault domain model |
| `security-vault-spi` | Vault persistence and cryptographic ports |
| `security-vault-application` | Vault use cases and orchestration |
| `security-vault-postgres` | PostgreSQL vault persistence adapter |
| `security-vault-crypto` | Envelope cryptography adapter |

## Ownership boundaries

- **Identity** owns canonical identity records, credentials' identity association, user/profile lifecycle and identity federation subject mapping. Security consumes identity/principal identifiers and authentication facts; it must not become a second user directory.
- **Security** owns authentication assurance, credential verification policy, session/security decisions, authorization policy evaluation, security-specific audit facts and vault secret protection.
- **Core** owns tenant lifecycle and trusted tenant context propagation. Security validates and consumes tenant context; it does not create a second tenant registry.
- **Social Graph** owns graph entities and relationship semantics. The Social Graph module remains in Core; this repository contains only an optional integration adapter.
- **Business capabilities** own their business audit facts. Security audit records cover security-relevant actions and decisions, not every business event.
- **Foundation** owns shared primitives. Do not duplicate Money, tenant IDs, common identifiers, clock, event envelope, or shared error contracts here.

## Dependency direction

```text
Core Foundation / Tenant Context
              |
              v
     Security Domain <- Identity contracts
              |
              v
        Security SPI
              |
              v
    Security Application
              |
       +------+------+
       |             |
       v             v
 Security Adapter  Vault Application
       |             |
       v          Vault SPI
   Quarkus/OIDC       |
                  +--+--+
                  |     |
                  v     v
              Postgres Crypto

Social Graph Adapter is optional and depends on Core Social Graph contracts.
Social Graph domain ownership does not move into this repository.
```

## Required package publication

Before enabling the independent Maven verification, publish and verify these artifacts from Core:

1. `tech.kayys.numou:numou-parent:0.1.0-SNAPSHOT`
2. `tech.kayys.numou:numou-bom:0.1.0-SNAPSHOT`
3. Foundation domain/application/adapter/testing artifacts used by the modules.
4. Cache API/adapter artifacts used by Security Application and Adapter.
5. Observability API/application artifacts used by Security Adapter.
6. Social Graph application and JDBC persistence artifacts used by the optional Social Graph Adapter.

The consuming workflow must authenticate to GitHub Packages using repository secrets or an authorized GitHub App. Never place a token in a POM, workflow literal, README, or committed Maven settings file.

## Cutover gates

- [ ] Core parent and platform BOM are published and resolvable from a clean runner.
- [ ] All required Core dependency artifacts are published at compatible versions.
- [ ] Run `mvn -B -ntp verify` from a clean checkout with an empty Maven local repository.
- [ ] All unit, integration, architecture and migration tests pass.
- [ ] Verify PostgreSQL vault migrations and Testcontainers tests.
- [ ] Verify cryptographic adapter tests, key-version metadata, rotation compatibility and failure behavior.
- [ ] Verify tenant isolation, cross-tenant denial and fail-closed behavior for missing/untrusted tenant context.
- [ ] Verify authentication and authorization behavior remains compatible with Identity and existing Core consumers.
- [ ] Publish Security BOM and module artifacts to this repository's GitHub Packages endpoint.
- [ ] Migrate Core and downstream consumers to the published Security artifacts.
- [ ] Remove duplicate monorepo source only in a separate, reviewed cutover PR after consumer migration is proven.

## Explicitly deferred

The legacy `vault-secret/` and `vault-secret-cloud/` source roots were not in the active Security Maven reactor and are not silently folded into this extraction. Review their code, dependencies, deployment model and compatibility separately before deciding whether they belong in this repository or in a dedicated external secret-provider integration.

## Release policy

Use one coordinated Security release train initially: publish the BOM and all ten modules with the same version. Keep the BOM artifact ID unique as `numou-security-bom`; never reuse the platform `numou-bom` artifact ID. Move to independently versioned modules only when there is a demonstrated compatibility and release-management need.
