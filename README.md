# Helm Values Validator

Lightweight docker container that validates Helm charts using the [kubeconform-helm](https://github.com/jtyr/kubeconform-helm) plugin and the [kubeconform](https://github.com/yannh/kubeconform) schema validation tool. It ensures that your Kubernetes manifests generated from Helm charts conform to Kubernetes schema standards.

---

## Features
- **Helm Plugin Integration**: Uses the `kubeconform-helm` plugin for  Helm chart validation.
- **Custom Values Support**: Validate charts with custom `values.yaml` files.
- **Verbose Reporting**: Provides detailed output with `--verbose` and `--summary` flags.
- **Configurable**: Supports `.kubeconform` files for custom validation settings.

---

## Prerequisites
- Docker installed on your system.
- Helm charts and `values.yaml` files ready for validation.

---

## Usage

### 1. Build the Docker Image
```bash
docker build -t helm-validator .
```

### 2. Run the Validator

```bash
docker run --rm \
    -v /path/to/chart:/chart \
    -v /path/to/values.yaml:/values.yaml \
    helm-validator /chart /values.yaml
```

Replace /path/to/chart with the path to your Helm chart directory and /path/to/values.yaml with your custom values file.

### Output

```
Validating Helm chart at '/chart' with values file '/values.yaml'...
Validation Output:
 stdin - PodDisruptionBudget release-name-loki-memcached-results-cache is valid
stdin - ServiceAccount loki is valid
stdin - ServiceAccount loki-canary is valid
stdin - PodDisruptionBudget release-name-loki-memcached-chunks-cache is valid
stdin - ConfigMap loki is valid
stdin - ConfigMap release-name-loki-gateway is valid
stdin - ConfigMap loki-runtime is valid
stdin - ClusterRole release-name-loki-clusterrole is valid
stdin - ClusterRoleBinding release-name-loki-clusterrolebinding is valid
stdin - Service release-name-loki-chunks-cache is valid
stdin - Service loki-memberlist is valid
stdin - Service loki-headless is valid
stdin - Service release-name-loki is valid
stdin - Service release-name-loki-gateway is valid
stdin - Service loki-canary is valid
stdin - Service release-name-loki-results-cache is valid
stdin - DaemonSet loki-canary is valid
stdin - StatefulSet release-name-loki-results-cache is valid
stdin - Deployment release-name-loki-gateway is valid
stdin - StatefulSet release-name-loki-chunks-cache is valid
stdin - StatefulSet release-name-loki is valid
stdin - Pod loki-helm-test is valid
Summary: 22 resources found parsing stdin - Valid: 22, Invalid: 0, Errors: 0, Skipped: 0

Validation completed successfully!
```

### Additional Config
#### `kubeconform` File
You can include a `.kubeconform` file in your Helm chart directory to customize validation. Example:
```yaml
schema-location:
  - default
  - https://my-schema-store/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json
summary: true
verbose: true
strict: true
```
This file is automatically used by the tool during validation.

## Development
### Build the Docker Image
```bash
docker build -t helm-validator .
```

## License
MIT License.

