
### Automatic Email Reply System Agents (Beta Version)

```markdown
# Automatic Email Reply System

## Project Overview
The Automatic Email Reply System is designed to automate the process of responding to customer emails for a fictional equipment rental service. It categorizes incoming emails, queries an SQL database for necessary information, and generates appropriate responses based on the content and category of the emails.

## Features
- **Email Categorization**: Automatically categorizes emails into predefined categories such as price inquiries, product questions, and customer feedback.
- **Database Queries**: Retrieves product information from an SQLite database based on the email queries.
- **Response Generation**: Uses a custom RAG (Retrieval-Augmented Generation) pipeline to generate contextually relevant responses.
- **CRM Integration**: Records issues and interactions in a CSV file for CRM purposes.

## Technologies Used
- Python 3.8+
- SQLite3 for the database
- Pandas for data handling
- GroqAPI for leveraging AI models
- Chroma for document retrieval in RAG pipeline

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Pip for package installation

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MathavanSG/EmailAutomation-AGENT.git
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
- Ensure the `.env` file is configured with the necessary API keys and database paths:
  ```plaintext
  GROQ_API_KEY=your_api_key_here
  DB_PATH=path_to_your_database.db
  ```

## Usage
To run the system:
```bash
python main.py
```
This script processes a batch of sample emails and demonstrates how the system categorizes and responds to different types of queries.

## Project Structure
- `create_and_populate_db.py`: Sets up the SQLite database and populates it with initial data.
- `crm.py`: Handles interactions with the customer relationship management system.
- `categorize_agent.py`, `email_writer.py`, `reviewer_agent.py`: Modules for categorizing emails, writing responses, and handling reviews.
- `utils.py`: Contains utility functions for email interaction and API authentication.
- `rag_agent.py`: Implements the RAG pipeline for response generation.
- `main.py`: The main script that ties all components together.

## Database Schema
The database schema includes the following table:
```plaintext
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    availability TEXT NOT NULL,
    price REAL NOT NULL
);
```

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
- Mathavan SG - [@MathavanSG](https://github.com/MathavanSG)

## Acknowledgments
- Thanks to GroqAPI for providing the AI model APIs.
- Special thanks to all contributors who participated in this project.
```

### Customizing Your README
Make sure to replace placeholders and add any additional details specific to your project. This includes updating links, specific commands, additional sections on how to contribute, report issues, or detailed explanations of more complex project features.
