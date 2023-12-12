import subprocess
import os
import shutil
import sys

class RepositoryManager:
    def __init__(self, repo_url, folder_name, doc_subpath):
        """
        Initialize the RepositoryManager with repository URL, folder name, and documentation subpath.

        :param repo_url: URL of the git repository.
        :param folder_name: Name of the folder where the repository will be cloned.
        :param doc_subpath: Subpath within the repository where documentation resides.
        """
        self.repo_url = repo_url
        self.folder_name = folder_name
        self.doc_folder_path = os.path.join(folder_name, doc_subpath)

    def clone_repo(self):
        """ Clone a specific folder from a git repository. """
        print(f"Cloning into {self.folder_name} from {self.repo_url}")
        subprocess.run(["git", "clone", self.repo_url, self.folder_name], check=True)

    def build_documentation(self):
        """ Build the documentation assuming Sphinx is used. """
        print(f"Building documentation in {self.doc_folder_path}")
        orig_directory = os.getcwd()
        os.chdir(self.doc_folder_path)
        print(f"Changed directory to: {self.doc_folder_path}")
        subprocess.run(["make", "html"], shell=True, check=True)
        os.chdir(orig_directory)

    def clean_folder(self):
        """ Delete a folder if it exists. """
        print(f"Attempting to clean folder: {self.folder_name}")
        if os.path.exists(self.folder_name):
            try:
                # Changing permissions to ensure deletion of all contents
                for root, dirs, files in os.walk(self.folder_name, topdown=False):
                    for name in files:
                        os.chmod(os.path.join(root, name), 0o666)
                    for name in dirs:
                        os.chmod(os.path.join(root, name), 0o666)
                shutil.rmtree(self.folder_name)
                print(f"Cleaned existing folder: {self.folder_name}")
            except Exception as e:
                print(f"Error cleaning the folder: {e}")
        else:
            print(f"Folder not found: {self.folder_name}")

    def clone_repo_and_build(self):
        """ Clone the repository and build its documentation. """
        print(f"Current directory: {os.getcwd()}")
        self.clean_folder()
        self.clone_repo()

        genai_module_path = os.path.join(self.folder_name, "src", "genai")
        if genai_module_path not in sys.path:
            sys.path.insert(0, genai_module_path)

        if not os.path.exists(self.doc_folder_path):
            print(f"Documentation folder not found at: {self.doc_folder_path}")
            return

        self.build_documentation()
        print("Documentation build is complete.")

if __name__ == "__main__":
    repo_url = "https://github.com/IBM/ibm-generative-ai.git"
    doc_folder_name = "ibm-generative-ai"
    doc_subpath = "documentation/docs"  # Use forward slashes for cross-platform compatibility

    manager = RepositoryManager(repo_url, doc_folder_name, doc_subpath)
    manager.clone_repo_and_build()
