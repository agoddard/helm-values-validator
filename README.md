# Helm Values Validator

Lightweight docker container that validates Helm charts using the [kubeconform-helm](https://github.com/jtyr/kubeconform-helm) plugin and the [kubeconform](https://github.com/yannh/kubeconform) schema validation tool. It ensures that your Kubernetes manifests generated from Helm charts conform to Kubernetes schema standards.

## Features
- **Helm Plugin Integration**: Uses the kubeconform-helm plugin for Helm chart validation
- **Custom Values Support**: Validate charts with custom values.yaml files
- **Remote Chart Support**: Validate charts directly from Helm repositories without manual downloads
- **Verbose Reporting**: Provides detailed output with --verbose and --summary flags
- **Configurable**: Supports .kubeconform files for custom validation settings

## Prerequisites
- Docker installed on your system
- Values file ready for validation

## Usage

### 1. Build the Docker Image
```bash
docker build -t helm-validator .
```

### 2. Run the Validator

The validator supports two modes of operation: local chart validation and remote chart validation.

#### Validating a Local Chart Directory:
If you have a local copy of a Helm chart, mount both the chart directory and your values file:
```bash
docker run --rm \
    -v /path/to/chart:/chart \
    -v /path/to/values.yaml:/values.yaml \
    helm-validator --local /chart
```

#### Validating a Remote Chart:
You can validate charts directly from Helm repositories without downloading them manually:
```bash
docker run --rm \
    -v /path/to/values.yaml:/values.yaml \
    helm-validator --remote <repo-name> <repo-url> <chart-name>
```

Example with Argo Workflows:
```bash
docker run --rm \
    -v ./my-values.yaml:/values.yaml \
    helm-validator --remote argo https://argoproj.github.io/argo-helm argo-workflows
```

This will:
1. Add the Helm repository
2. Download the specified chart
3. Validate it against your values file

### Example Output

```
Adding Helm repository 'argo' from https://argoproj.github.io/argo-helm...
Updating Helm repositories...
Pulling chart 'argo/argo-workflows'...
Chart extracted to: /tmp/helm-charts/argo-workflows
Validating Helm chart with values file '/values.yaml'...
Validation Output:
 stdin - ServiceAccount argo is valid
 stdin - ConfigMap argo-workflows-config is valid
 [...]
Summary: 22 resources found parsing stdin - Valid: 22, Invalid: 0, Errors: 0, Skipped: 0

Validation completed successfully!
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

## Common Helm Repository Examples

Here are some common Helm repositories and their charts:

```bash
# Argo Workflows
docker run --rm \
    -v ./argo-values.yaml:/values.yaml \
    helm-validator --remote argo https://argoproj.github.io/argo-helm argo-workflows

# Prometheus Stack
docker run --rm \
    -v ./prometheus-values.yaml:/values.yaml \
    helm-validator --remote prometheus-community https://prometheus-community.github.io/helm-charts kube-prometheus-stack

# Cert Manager
docker run --rm \
    -v ./certmanager-values.yaml:/values.yaml \
    helm-validator --remote jetstack https://charts.jetstack.io cert-manager
```

## License
MIT License.