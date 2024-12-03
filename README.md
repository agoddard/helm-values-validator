# Helm Values Validator

Lightweight docker container that validates Helm charts using the [kubeconform-helm](https://github.com/jtyr/kubeconform-helm) plugin and the [kubeconform](https://github.com/yannh/kubeconform) schema validation tool. It ensures that your Kubernetes manifests generated from Helm charts conform to Kubernetes schema standards.

## Features
- **Helm Plugin Integration**: Uses the kubeconform-helm plugin for Helm chart validation
- **Custom Values Support**: Validates charts with multiple values files, merged in the order specified
- **Remote Chart Support**: Validate charts directly from Helm repositories without manual downloads
- **Verbose Reporting**: Provides detailed output with --verbose and --summary flags
- **Configurable**: Supports .kubeconform files for custom validation settings

## Prerequisites
- Docker installed on your system
- Values files ready for validation

## Usage

### 1. Build the Docker Image
```bash
docker build -t helm-validator .
```

### 2. Run the Validator

The validator supports two modes of operation: local chart validation and remote chart validation. Values files are merged in the order they are mounted.

#### Validating a Local Chart Directory:
```bash
docker run --rm \
    -v /path/to/chart:/chart \
    -v /path/to/base.yaml:/values-0 \
    -v /path/to/env.yaml:/values-1 \
    -v /path/to/overrides.yaml:/values-2 \
    helm-validator --local /chart
```

#### Validating a Remote Chart:
```bash
docker run --rm \
    -v /path/to/base.yaml:/values-0 \
    -v /path/to/env.yaml:/values-1 \
    -v /path/to/overrides.yaml:/values-2 \
    helm-validator --remote <repo-name> <repo-url> <chart-name>
```

Values files are merged in the order specified by their mount points (/values-0, /values-1, etc.), with later files taking precedence.

### Example Output

```
Adding Helm repository 'argo' from https://argoproj.github.io/argo-helm...
Updating Helm repositories...
Pulling chart 'argo/argo-workflows'...
Chart extracted to: /tmp/helm-charts/argo-workflows

Values files (in merge order):
  - 00-values.yaml (from /values-0)
  - 01-values.yaml (from /values-1)
  - 02-values.yaml (from /values-2)

Validating Helm chart...
Validation Output:
 stdin - ServiceAccount argo is valid
 stdin - ConfigMap argo-workflows-config is valid
 [...]
Summary: 22 resources found parsing stdin - Valid: 22, Invalid: 0, Errors: 0, Skipped: 0

Validation completed successfully!
```

## Common Examples

### Argo Workflows with environment overlays:
```bash
docker run --rm \
    -v ./base.yaml:/values-0 \
    -v ./prod.yaml:/values-1 \
    helm-validator --remote argo https://argoproj.github.io/argo-helm argo-workflows
```

### Prometheus Stack with multiple configurations:
```bash
docker run --rm \
    -v ./defaults.yaml:/values-0 \
    -v ./storage.yaml:/values-1 \
    -v ./alerts.yaml:/values-2 \
    helm-validator --remote prometheus-community https://prometheus-community.github.io/helm-charts kube-prometheus-stack
```

### Cert Manager with different issuers:
```bash
docker run --rm \
    -v ./base.yaml:/values-0 \
    -v ./cluster-issuers.yaml:/values-1 \
    helm-validator --remote jetstack https://charts.jetstack.io cert-manager
```

### Additional Config
#### kubeconform File
You can include a .kubeconform file in your Helm chart directory to customize validation. Example:
```yaml
schema-location:
  - default
  - https://my-schema-store/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json
summary: true
verbose: true
strict: true
```

This file is automatically used by the tool during validation.

## License
MIT License.