import pandas as pd
import os

def add_customer_data(email):
    # Define the file path
    file_path = 'issues.csv'
    
    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, read the existing data
        issues_df = pd.read_csv(file_path)
    else:
        # If it does not exist, create an empty DataFrame
        issues_df = pd.DataFrame(columns=['subject', 'body'])
    
    # Append the new issue
    issues_df = issues_df.append({'subject': email['subject'], 'body': email['body']}, ignore_index=True)
    
    # Save the updated DataFrame back to the CSV
    issues_df.to_csv(file_path, index=False)

    return "Issue has been noted down. Will notify the CRM team to contact you."
