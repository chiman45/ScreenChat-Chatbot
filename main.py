import tkinter as tk
from tkinter import scrolledtext, PhotoImage
from tkinter import font as tkfont
import requests
from bs4 import BeautifulSoup


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SereneChat")
        
        # Set the icon (logo)
        self.logo = PhotoImage(file='img.png')
        self.root.iconphoto(False, self.logo)
        
        # Set the background color of the root window
        self.root.configure(bg='black')

        # Define the font
        self.font_family = 'Helvetica'
        self.font_size = 12
        self.font = tkfont.Font(family=self.font_family, size=self.font_size)

        # Create chat area
        self.chat_area = scrolledtext.ScrolledText(
            root, state='disabled', wrap='word', height=20, width=60,
            bg='black', fg='white', insertbackground='white',
            font=self.font
        )
        self.chat_area.pack(padx=10, pady=10)
        
        # Create input area
        self.entry = tk.Entry(
            root, width=50, bg='black', fg='white', insertbackground='white',
            font=self.font
        )
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack(padx=10, pady=5, side='left')
        
        # Create send button
        self.send_button = tk.Button(
            root, text="Send", command=self.send_message,
            bg='black', fg='white', activebackground='grey',
            font=self.font
        )
        self.send_button.pack(padx=10, pady=5, side='right')
    
    def send_message(self, event=None):
        user_input = self.entry.get()
        if user_input:
            self.display_message(f"You: {user_input}\n")
            # Get response from the search function
            response = self.get_chatbot_response(user_input)
            self.display_message(f"\nChatbot: {response}\n")
            self.entry.delete(0, tk.END)
    
    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)
    
    def get_chatbot_response(self, user_input):
        # Use the search function to get a response
        return search_query(user_input)

def search_query(query):
    # Construct the search URL
    search_url = f"https://www.google.com/search?q={query}"
    
    # Send the GET request to the search URL
    response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    
    # Check if the request was successful
    if response.status_code != 200:
        return "Error: Unable to fetch search results."
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the search result snippets
    snippets = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
    
     # Extract and combine the text of the first few snippets
    combined_text = ""
    for snippet in snippets[:5]:  # Adjust the number as needed to get around 100 words
        combined_text += snippet.get_text() + " "
        if len(combined_text.split()) > 100:
            break
    
    # Trim the text to around 100 words
    combined_text_words = combined_text.split()
    if len(combined_text_words) > 100:
        combined_text = " ".join(combined_text_words[:100])
    
    return combined_text or "No results found."

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
