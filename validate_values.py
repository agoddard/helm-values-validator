import os
import subprocess
import sys

def validate_with_helm_plugin(chart_path, values_file, namespace="default"):
    try:
        result = subprocess.run(
            [
                "helm", "kubeconform",
                "--namespace", namespace,
                "-f", values_file,
                "--verbose", "--summary",
                chart_path
            ],
            check=True,
            capture_output=True
        )
        print("Validation Output:\n", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Validation failed with error:\n", e.stderr.decode())
        sys.exit(1)

def main(chart_path, values_file):
    print(f"Validating Helm chart at '{chart_path}' with values file '{values_file}'...")
    validate_with_helm_plugin(chart_path, values_file)
    print("Validation completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_values.py <helm-chart-path> <values.yaml>")
        sys.exit(1)

    helm_chart_path = sys.argv[1]
    values_yaml = sys.argv[2]

    if not os.path.exists(helm_chart_path):
        print(f"Error: Helm chart path '{helm_chart_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists(values_yaml):
        print(f"Error: values.yaml file '{values_yaml}' does not exist.")
        sys.exit(1)

    main(helm_chart_path, values_yaml)

