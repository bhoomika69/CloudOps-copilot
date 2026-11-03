
from pathlib import Path

# Finding the project folder and incident folder
project_folder = Path(__file__).resolve().parent.parent
incident_folder = project_folder / "data" / "incidents"


def load_incidents():
    incident_data = []

    # Reading all incident files one by one
    for file in incident_folder.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            report = f.read()

        incident_data.append({
            "filename": file.name,
            "content": report
        })

    return incident_data


# Starting the data loading process
if __name__ == "__main__":
    incidents = load_incidents()

    print("Welcome to CloudOps Copilot!")
    print("Incident reports loaded:", len(incidents))

    for incident in incidents:
        print("\nFile:", incident["filename"])
        print(incident["content"])
        print("-" * 40)
