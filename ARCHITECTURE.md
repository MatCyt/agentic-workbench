# Architecture — <Project Name>
    Stable facts only. Sections are optional - most of them depends on the specific project.
 
## Project Purpose
    What the system does. Shortly.
 
## Project Rules
    General development, deployment rules that are project specific and should not be in AGENTS.md

## System Overview
    Major applications, services, data stores, and external systems and how they connect. 
    A small diagram (Mermaid) is enough.

## Tech stack
    High level description of the stack in the project.

## Common Patterns
    How shared functionality is handled in this repo (ex. config loading, DB access, alerting, auth)
    Ideally with pointers to canonical examples like "see packages/db/client.py"

## Infra and Deployment
    Where it runs, how to deploy, how to access dev and prod.
    Keep few lines, if more then move this to a different file and reference.
 
## Commands and Verification
    Project-specific commands beyond the standard `make` targets, and the definition of done for this repo
 
## Project Workflows
    Numbered steps for recurring multi-step tasks, e.g. *Adding a service*: copy template, add `.env.example`, add Makefile ...
 
## Domain Glossary
    Project-specific terms that are not obvious. Could be moved and referenced if longer.
 
## Code Map
    Top-level directory layout with one line per directory stating what lives there and what it is responsible for.
 
## Key Services
    One block per service: responsibilities, locked decision, non-obvious info.
    Highly optional, might be in a dedicated README.
 
## Key Architectural Decisions
    One or two sentences each for locked-in decisions that are not obvious from the code.
    Highly optional.
 
## Data Flow
    Sources → stores → consumers, in one paragraph or one diagram. 
    Optional - depending on the project type.
 
## Related Docs
    Pointers to other relevant project files (service READMEs, runbooks, ADRs, external API contracts).
