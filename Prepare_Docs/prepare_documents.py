import os
import json
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader


class SunbeamJSONLoader(BaseLoader):
    """
    Custom LangChain Loader for Sunbeam scraped JSON data.
    Converts structured JSON into clean, LLM-friendly text Documents.
    """

    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load(self):
        documents = []

        about_path = os.path.join(self.data_dir, "about_us.json")
        if os.path.exists(about_path):
            with open(about_path, "r", encoding="utf-8") as f:
                about_data = json.load(f)

            for para in about_data.get("about_sunbeam", []):
                documents.append(
                    Document(
                        page_content=para.strip(),
                        metadata={
                            "source": "about_sunbeam",
                            "category": "about"
                        }
                    )
                )

        branches_path = os.path.join(self.data_dir, "branches.json")
        if os.path.exists(branches_path):
            with open(branches_path, "r", encoding="utf-8") as f:
                branches = json.load(f)

            for branch_name, content in branches.items():
                text = f"""
                Branch Name: {branch_name}
                Details:
                {content}
                """
                documents.append(
                    Document(
                        page_content=text.strip(),
                        metadata={
                            "source": "branch",
                            "branch_name": branch_name,
                            "category": "branch"
                        }
                    )
                )

        courses_path = os.path.join(self.data_dir, "modular_courses.json")
        if os.path.exists(courses_path):
            with open(courses_path, "r", encoding="utf-8") as f:
                courses = json.load(f)

            for course in courses:
                text = f"""
                Course Name: {course.get('name')}
                Duration: {course.get('duration')}
                Description:
                {course.get('content')}
                More Information: {course.get('url')}
                """
                documents.append(
                    Document(
                        page_content=text.strip(),
                        metadata={
                            "source": "modular_course",
                            "course_name": course.get("name"),
                            "category": "course"
                        }
                    )
                )

        internship_path = os.path.join(self.data_dir, "sunbeam_internship.json")
        if os.path.exists(internship_path):
            with open(internship_path, "r", encoding="utf-8") as f:
                internship_data = json.load(f)

            programs = internship_data.get("available_programs", [])

            for idx, program in enumerate(programs):

                if idx == 0:
                    continue

                lines = []
                for key, value in program.items():
                    if value:
                        lines.append(f"{key}: {value}")

                documents.append(
                    Document(
                        page_content="Internship Program Details:\n" + "\n".join(lines),
                        metadata={
                            "source": "internship",
                            "section": "available_programs",
                            "technology": program.get("Technology", "").strip()
                        }
                    )
                )

            structures = internship_data.get("training_structure", [])

            for idx, row in enumerate(structures):
                if idx == 0:
                    continue

                lines = []
                for key, value in row.items():
                    if value:
                        lines.append(f"{key}: {value}")

                documents.append(
                    Document(
                        page_content="Internship Training Structure:\n" + "\n".join(lines),
                        metadata={
                            "source": "internship",
                            "section": "training_structure"
                        }
                    )
                )

            batches = internship_data.get("batch_schedule", [])

            for idx, batch in enumerate(batches):
                if idx == 0:
                    continue

                lines = []
                for key, value in batch.items():
                    if value:
                        lines.append(f"{key}: {value}")

                documents.append(
                    Document(
                        page_content="Internship Batch Schedule:\n" + "\n".join(lines),
                        metadata={
                            "source": "internship",
                            "section": "batch_schedule",
                            "batch": batch.get("Batch", "")
                        }
                    )
                )

        return documents


if __name__ == "__main__":
    loader = SunbeamJSONLoader(data_dir="data")
    documents = loader.load()

    print(f"Loaded {len(documents)} documents\n")

    for i, doc in enumerate(documents[:45]):
        print(f"--- Document {i+1} ---")
        print(doc.page_content)
        print("Metadata:", doc.metadata)
        print()
