import os
import subprocess
import sys
import tempfile
import shutil

def add_helm_repo(repo_name, repo_url):
    try:
        print(f"Adding Helm repository '{repo_name}' from {repo_url}...")
        subprocess.run(
            ["helm", "repo", "add", repo_name, repo_url],
            check=True,
            capture_output=True
        )
        print("Updating Helm repositories...")
        subprocess.run(
            ["helm", "repo", "update"],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error adding Helm repository:\n{e.stderr.decode()}")
        sys.exit(1)

def fetch_chart(repo_name, chart_name, target_dir):
    try:
        print(f"Pulling chart '{repo_name}/{chart_name}'...")
        # Pull the chart
        subprocess.run(
            ["helm", "pull", f"{repo_name}/{chart_name}", "--untar", "--untardir", target_dir],
            check=True,
            capture_output=True
        )
        
        chart_path = os.path.join(target_dir, chart_name)
        if not os.path.exists(chart_path):
            contents = os.listdir(target_dir)
            if len(contents) == 1:
                chart_path = os.path.join(target_dir, contents[0])
            else:
                raise Exception(f"Unexpected chart directory structure: {contents}")
        
        print(f"Chart extracted to: {chart_path}")
        return chart_path
    except subprocess.CalledProcessError as e:
        print(f"Error fetching Helm chart:\n{e.stderr.decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing chart: {str(e)}")
        sys.exit(1)

def validate_with_helm_plugin(chart_path, values_file, namespace="default"):
    try:        
        print(f"\nRunning validation...")
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

def main():
    values_yaml = "/values.yaml"
    if not os.path.exists(values_yaml):
        print(f"Error: values.yaml file not found at {values_yaml}. Please mount your values file to /values.yaml")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("""
Usage: 
    For local charts:
        python validate_values.py --local <helm-chart-path>
    For remote charts:
        python validate_values.py --remote <repo-name> <repo-url> <chart-name>
        
Example:
    Local:  python validate_values.py --local /chart
    Remote: python validate_values.py --remote argo https://argoproj.github.io/argo-helm argo-workflows
        """)
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "--local":
        if len(sys.argv) != 3:
            print("Error: Local mode requires chart path")
            sys.exit(1)
        
        helm_chart_path = sys.argv[2]
        if not os.path.exists(helm_chart_path):
            print(f"Error: Helm chart path '{helm_chart_path}' does not exist.")
            sys.exit(1)
            
    elif mode == "--remote":
        if len(sys.argv) != 5:
            print("Error: Remote mode requires repo name, repo URL, and chart name")
            sys.exit(1)
        
        repo_name = sys.argv[2]
        repo_url = sys.argv[3]
        chart_name = sys.argv[4]

        print(f"Adding Helm repository '{repo_name}' from {repo_url}...")
        add_helm_repo(repo_name, repo_url)
        
        chart_dir = "/tmp/helm-charts"
        os.makedirs(chart_dir, exist_ok=True)
        
        print(f"Fetching chart '{chart_name}' from repository...")
        helm_chart_path = fetch_chart(repo_name, chart_name, chart_dir)
        
        if not os.path.exists(helm_chart_path):
            print(f"Error: Failed to locate chart at {helm_chart_path}")
            sys.exit(1)
            
        print(f"Using chart from: {helm_chart_path}")
    else:
        print(f"Error: Invalid mode '{mode}'. Use --local or --remote")
        sys.exit(1)

    print(f"Validating Helm chart at '{helm_chart_path}' with values file '{values_yaml}'...")
    validate_with_helm_plugin(helm_chart_path, values_yaml)
    print("Validation completed successfully!")

if __name__ == "__main__":
    main()