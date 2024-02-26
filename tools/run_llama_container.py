import subprocess

def run_docker_command():
    command = [
        "docker", "run", "-d", "--gpus=all",
        "-v", "ollama:/root/.ollama",
        "-p", "11434:11434",
        "-e", "OLLAMA_ORIGINS=*",
        "--name", "ollama",
        "ollama/ollama"
    ]

    try:
        subprocess.run(command, check=True)
        print("Docker container started successfully.")
    except subprocess.CalledProcessError as e:
        print("Error running Docker command:", e)

# Call the function to run the Docker command
run_docker_command()