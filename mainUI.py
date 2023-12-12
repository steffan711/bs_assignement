from repoManager import RepositoryManager
from parserHTML import HTMLParser
from pineconeManager import PineconeManager
from chatAgent import ChatAgent

import pprint
import os
import streamlit as st

class AIAssistantApp:
    """
    Class to represent an AI Assistant Application using Streamlit.
    """

    def __init__(self):
        """
        Initialize the AI Assistant application and its components.
        """
        self.initialize_ai_agent()

    def initialize_ai_agent(self):
        """
        Initializes the AI agent and related resources. Sets up session state variables.
        """
        if 'initialized' not in st.session_state:
            st.session_state['initialized'] = True
            st.session_state['stored_text'] = ""
            try:
                model_name = 'text-embedding-ada-002'
                pine_api_key = "PINE_API_KEY"
                openai_api_key = "OPENAI_API_KEY"
                environment = "gcp-starter"
                index_name = 'ibm-generative-ai-doc'
                metric = 'dotproduct'
                dimension = 1536
                text_field = "text"

                pineconeMan = PineconeManager(model_name, pine_api_key, openai_api_key,
                                          environment, index_name, metric, dimension, text_field)

                if not pineconeMan.index_not_empty():
                    repo_url = "https://github.com/IBM/ibm-generative-ai.git"
                    doc_folder_name = "ibm-generative-ai"
                    doc_subpath = os.path.join("documentation", "docs")

                    repoMan = RepositoryManager(repo_url, doc_folder_name, doc_subpath)
                    repoMan.clone_repo_and_build()

                    parser = HTMLParser()
                    doc_folder_path = os.path.join(doc_folder_name, "documentation", "docs", "build", "html")
                    website_address = "https://ibm.github.io/ibm-generative-ai/"

                    data_with_citations = parser.crawl_website(doc_folder_path, website_address)
                    pineconeMan.fill_index(data_with_citations)

                st.session_state['agent'] = ChatAgent(openai_api_key, pineconeMan.vectorstore)

            except Exception as e:
                st.session_state['stored_text'] = "<b>Error occurred:</b><br>" + str(e) + "<br>"

    def display_ui(self):
        """
        Sets up and displays the Streamlit user interface.
        """
        st.title("AI Assistant Interface")

        # Initialize session state variables
        self.initialize_ai_agent()

        # CSS for styling the conversation container
        st.markdown("""
                    <style>
                    .scrollable-container {
                        height: 200px;
                        overflow-y: scroll;
                    }
                    </style>
                    """, unsafe_allow_html=True)

        # Display conversation area
        st.markdown("### Conversation:")
        st.markdown(f"<div class='scrollable-container'>{st.session_state['stored_text']}</div>",
                    unsafe_allow_html=True)

        # Query input area
        st.markdown("### Enter your query here:", unsafe_allow_html=True)
        st.text_area(" ", key="user_input", height=60)

        # Submit button
        st.button("Submit", on_click=self.handle_submit)

    def handle_submit(self):
        """
        Handles the submission of queries and updates the conversation display.
        """
        try:
            ai_response_dict = st.session_state['agent'].run(st.session_state.user_input)
            pprint.pprint(ai_response_dict)

            answer = ai_response_dict.get('answer', 'No answer provided.')
            sources = '\n'.join(ai_response_dict.get('sources', []))

            st.session_state['stored_text'] += (
                    f"<b>You:</b> {st.session_state.user_input}<br>"
                    f"<b>AI Agent:</b> {answer}<br>"
                    + (f"<i>Sources:</i><br>{sources}<br><br>" if sources else "<br>")
            )
        except Exception as e:
            st.session_state['stored_text'] += f"<br><b>Error occurred:</b><br>{str(e)}<br>"

        # Clear the input field
        st.session_state['user_input'] = ""


if __name__ == "__main__":
    app = AIAssistantApp()
    app.display_ui()
