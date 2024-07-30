# rag_agent.py

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the language model
llm = ChatGroq(api_key=api_key)

# Initialize the embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Function to split text into chunks
def split_chunks(text):
    text_splitter = SemanticChunker(embedding_function)
    docs = text_splitter.create_documents([text])
    return docs

# Example text
text = """Frequently Asked Questions about Film Equipment

Cameras

What are the different types of cameras used in filmmaking?
DSLR Cameras: Commonly used for their versatility and image quality.
Mirrorless Cameras: Known for being lightweight with high video quality.
Cinema Cameras: Specifically designed for high-end film production with superior image quality and extensive manual controls.
Action Cameras: Compact and durable, used for capturing action shots.
Camcorders: Traditional video cameras, often used for documentary and news production.
What is the difference between full-frame and crop sensor cameras?
Full-Frame Cameras: Have a sensor size equivalent to 35mm film, offering better low-light performance and wider field of view.
Crop Sensor Cameras: Have smaller sensors, which results in a narrower field of view and generally less low-light capability, but can be more affordable.
How do I choose the right camera for my project?
Consider the type of project (e.g., documentary, narrative, action).
Assess the budget and available lenses.
Evaluate the camera's resolution and frame rate capabilities.
Look into the camera's ergonomics and durability.
Lenses

What are the different types of lenses used in filmmaking?
Prime Lenses: Fixed focal length lenses known for their sharpness and wide apertures.
Zoom Lenses: Variable focal length lenses that offer versatility in framing shots without changing the lens.
Wide-Angle Lenses: Capture a broad field of view, ideal for landscapes and tight spaces.
Telephoto Lenses: Offer a narrow field of view and are used for close-ups and distant subjects.
Macro Lenses: Designed for extreme close-ups with high detail.
How do I choose the right lens for my project?
Determine the desired focal length based on the shot composition.
Consider the aperture size for low-light performance and depth of field control.
Look at the lens build quality and compatibility with your camera.
Lighting

What types of lights are commonly used in film production?
Tungsten Lights: Provide a warm, continuous light, often used indoors.
LED Lights: Energy-efficient, versatile, and available in various color temperatures.
Fluorescent Lights: Offer soft, even lighting, suitable for studio setups.
HMI Lights: Powerful daylight-balanced lights used for outdoor and high-intensity lighting.
Softboxes: Diffuse light for a soft, even illumination.
How do I set up basic three-point lighting?
Key Light: The main source of light, placed at a 45-degree angle to the subject.
Fill Light: Positioned opposite the key light to reduce shadows.
Back Light: Placed behind the subject to create separation from the background.
Audio Equipment

What types of microphones are used in film production?
Lavalier Microphones: Small, clip-on mics ideal for dialogue.
Shotgun Microphones: Directional mics mounted on boom poles, used for capturing dialogue from a distance.
Handheld Microphones: Used for interviews and live reporting.
Condenser Microphones: Studio-quality mics for high-fidelity audio recording.
How do I choose the right microphone for my project?
Lavalier Mics for discreet and close-up dialogue recording.
Shotgun Mics for capturing focused sound from a distance.
Handheld Mics for interviews and on-the-go recording.
Condenser Mics for controlled studio environments.
Accessories

What are essential accessories for film production?
Tripods and Monopods: For stable camera support.
Gimbals and Stabilizers: To achieve smooth, cinematic shots.
Camera Rigs and Shoulder Mounts: For handheld shooting stability.
External Monitors: For better viewing and framing.
Follow Focus Systems: For precise focus control.
Filters (ND, Polarizers): To control exposure and reflections.
How do I properly maintain my film equipment?
Regularly clean lenses and sensors with appropriate tools.
Store equipment in a dry, dust-free environment.
Check cables and connections for wear and tear.
Update firmware for cameras and accessories as needed.
Transport equipment in padded cases to prevent damage.
Post-Production

What software is commonly used for editing film?
Adobe Premiere Pro: A popular choice for professional video editing.
Final Cut Pro X: Favored by many Mac users for its intuitive interface.
DaVinci Resolve: Known for its advanced color grading capabilities.
Avid Media Composer: Preferred by many film studios for its robust editing features.
What is color grading, and why is it important?
Color Grading: The process of altering and enhancing the color of a film.
Importance: It sets the mood, enhances the visual storytelling, and ensures consistency across all shots."""

# Function to initialize the Chroma database
def initialize_chroma_db(text, embedding_function, persist_directory="./chroma_db"):
    if not os.path.exists(persist_directory):
        chunks = split_chunks(text)
        db = Chroma.from_texts(chunks, embedding_function, persist_directory=persist_directory)
    else:
        db = Chroma(persist_directory=persist_directory)
    return db

# Initialize the Chroma database
db2 = initialize_chroma_db(text, embedding_function)
retriever = db2.as_retriever()

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="Given the context: {context},answer the question: {question} If no solution is found, escalate the issue to customer service."
)
def retrieve_similar_documents(query, persist_directory, top_k):
    """Retrieve similar documents from Chroma."""
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
    docs = db.similarity_search(query, k=top_k)
    return docs
# Create the RAG chain using RunnableSequence
rag_chain = prompt_template | llm | StrOutputParser()

def get_rag_output(query):
    persist_directory="./chroma_db"
    context = retrieve_similar_documents(query,persist_directory,3)
    response = rag_chain.invoke({"context": context, "question": query})
    return response
