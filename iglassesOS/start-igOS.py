import subprocess
import time



def run_program(program):
    try:
        subprocess.run(program, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite : {e}")

def main():
    # Premier programme à exécuter
    program1 = ["python", "system/root/edx-explorer/edx-xpl.py"]
    run_program(program1)

    # Attendre l'interaction utilisateur pendant 3 secondes
    print("Attente de 3 secondes...")
    time.sleep(3)

    # Deuxième programme à exécuter
    program2 = ["python", "MAIA/launch"]
    run_program(program2)

if __name__ == "__main__":
    main()

