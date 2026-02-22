# Outputs

Generated outputs from Qwen Code workflows.

## Purpose

This directory stores artifacts generated during Qwen Code sessions:

- Implementation reports
- System review reports
- Execution reports
- Other generated documentation

## Usage

Outputs are typically created by commands like:

```bash
# Generate implementation report
> /execution-report

# Generate system review
> /system-review requests/my-feature-plan.md
```

## Directory Structure

```
08-outputs/
├── README.md              # This file
├── implementation-reports/ # Implementation reports
├── system-reviews/        # System review reports
└── execution-reports/     # Execution reports
```

## Related Directories

- **[requests/](../../requests/)** — Input plans and PRDs (at project root)
- **[03-templates](../03-templates/)** — Templates for output formats
