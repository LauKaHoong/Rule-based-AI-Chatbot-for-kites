from flask import Flask, request, render_template, jsonify
import re
from Chatbot import Chatbot, get_synonyms_datamuse
import json
import os

greetings = get_synonyms_datamuse("hello", "UH")
history = get_synonyms_datamuse ("tale", "n")
competition = get_synonyms_datamuse ("contest", "n")
material = get_synonyms_datamuse("material", "n")
design = get_synonyms_datamuse("design", "n")
flying = get_synonyms_datamuse("flying", "v")
famous = get_synonyms_datamuse("famous", "a")
events = get_synonyms_datamuse("event", "n")
weather = get_synonyms_datamuse("weather", "n")
technique = get_synonyms_datamuse("technique", "n") 
symbol = get_synonyms_datamuse("symbol", "v")
craftsmanship = get_synonyms_datamuse("craftsmanship", "n")
environment = get_synonyms_datamuse("environment", "n")
emotions = get_synonyms_datamuse("emotion", "n")

rule = { # the number is to set the priority 
    2: {
    re.compile(rf"(?i)\b(what|about)\b.*\bpakpaokite\b"): [
        "The Pakpao kite is a traditional Thai kite known for its role in Thai kite competitions, representing the 'female' kite.",
        "Pakpao kites have a unique diamond shape and long tail, allowing them to maneuver skillfully in the air.",
        "The craftsmanship of Pak Pao kites is a beautiful expression of Thai cultural heritage."
    ],
},
    1:{
    re.compile(rf"(?i)\b({'|'.join(material)})\b"): [
        "PakPao Kites are traditionally made from bamboo and paper, reflecting Thailand's rich craftsmanship.",
        "The materials used for PakPao kites, mainly bamboo and paper, showcase a rich tradition of kite making in Thailand.",
        "Modern variations of Pak Pao kites may incorporate materials like fabric and plastic for added durability."
    ],
    
    re.compile(rf"(?i)\b({'|'.join(history)})\b"): [
        "Pakpao kites date back to the Sukhothai and Rattanakosin periods in Thailand, where kite flying was a royal sport.",
        "Kite flying became a popular pastime in Thailand during the Sukhothai and Rattanakosin periods, often supported by kings.",
        "The rich history of Pak Pao kites reflects the cultural evolution of kite-making techniques in Thailand."
    ],
    
    re.compile(rf"(?i)\b({'|'.join(competition)})\b"): [
        "In Thai kite-fighting competitions, Pakpao kites are flown by teams and designed with long tails to capture larger Chula kites.",
        "These contests symbolize the rivalry between Pakpao and Chula kites, highlighting agility versus strength.",
        "Competitions are not just about flying; they showcase artistic designs and team strategy."
    ],
    
        re.compile(rf"(?i)\b({'|'.join(flying)})\b"): [
        "To launch a Pak Pao kite, you need a clear space and some wind to help it soar.",
        "Flying a kite is not just fun; it requires skill to control its movements in the air.",
        "The art of flying Pak Pao kites combines tradition with the thrill of the chase in the sky."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(famous)})\b"): [
        "The Pak Pao kite is one of the most famous types of kites in Thailand, cherished for its design and agility.",
        "Many artisans are renowned for their Pak Pao kite creations, showcasing exceptional craftsmanship."
    ],
    
        re.compile(rf"(?i)\b({'|'.join(design)})\b"): [
        "Pak Pao kites are often decorated with bright colors and intricate patterns.",
        "The colors used in Pak Pao kites can symbolize various aspects of Thai culture and beliefs."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(events)})\b"): [
        "Kite flying events are often held during festivals in Thailand, bringing together enthusiasts from all over.",
        "During festivals, you can witness spectacular displays of Pak Pao kites against the sky.",
        "The kite festival in Thailand is a vibrant celebration of culture, tradition, and community."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(weather)})\b"): [
        "The best weather for flying kites is usually sunny with a gentle breeze.",
        "Pak Pao kites thrive in windy conditions, so a breezy day is perfect for flying!",
        "Rainy or stormy weather is not ideal for kite flying, as it can be dangerous.",
        "A clear blue sky and a steady wind make for the perfect kite-flying experience."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(technique)})\b"): [
        "Kite-making requires precise craftsmanship and an understanding of aerodynamics.",
        "The techniques for flying a Pak Pao kite involve knowing how to read the wind and control the string.",
        "Mastering the art of kite flying can take time, but it's incredibly rewarding.",
        "Artisans spend years perfecting their skills in traditional kite-making techniques."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(symbol)})\b"): [
        "Pak Pao kites symbolize freedom and joy, soaring high in the sky.",
        "In Thai culture, kites often represent good luck and are a sign of prosperity.",
        "The designs and colors of Pak Pao kites can convey different meanings and stories."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(craftsmanship)})\b"): [
        "The craftsmanship behind Pak Pao kites is a blend of art and engineering.",
        "Each kite is carefully crafted by skilled artisans who take pride in their work.",
        "Pak Pao kites are often handmade, reflecting the dedication and skill of their creators."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(environment)})\b"): [
        "Flying kites is best enjoyed in open fields or areas free from obstacles.",
        "The beauty of flying Pak Pao kites is enhanced by the natural environment.",
        "An ideal outdoor setting adds to the enjoyment of the kite-flying experience."
    ],
        
        re.compile(rf"(?i)\b({'|'.join(emotions)})\b"): [
        "Many people feel a sense of joy and freedom when flying kites.",
        "The experience of watching kites dance in the sky can be quite thrilling.",
        "Kite flying can evoke feelings of nostalgia and happiness, especially during festivals."
    ],
    },
    3:{
    re.compile(rf"(?i)\b({'|'.join(greetings)})\b"): [
        "How are you?",
        "Are you doing okay?",
        "Hello! What's on your mind?",
        "Greetings! How can I assist you today?",
        "Hi there! Ready to learn about Pak Pao kites?",
        "Welcome! What would you like to discuss today?"
    ],
    
    re.compile(r".*") : [ # anything other than the intent
        "I'm not sure I understand. Can you ask something else?",
        "Could you rephrase that? I'm here to help!",
        "That’s interesting, but I’m not certain how to respond."
    ]
    },
 
}

app = Flask(__name__, template_folder='views')

@app.route("/")
def index ():
    return render_template('index.html')    

@app.route('/puzzle')
def puzzle():
    return render_template('puzzle.html')

@app.route('/quizz')
def quiz():
    return render_template('quiz.html')

@app.route('/test_quiz', methods=['GET'])
def test_quiz():
    return "This is a test route for quiz."

@app.route("/ChatBot", methods = ["POST"])
def chat ():
    data = request.json
    if data is None:
        return jsonify({'output': 'Invalid request'})
    
    user_input = data.get('textarea')
    username = data.get('name')
    priority_rule = data.get('priority', 0)
    chatbot = Chatbot(user_input, rule, username, priority_rule)
    ProcessText = chatbot.correct_spell(user_input)
    keyMatching, times_asking = chatbot.key_match()
    text = "".join (ProcessText)
    return jsonify ({'output': keyMatching, 'input' : text, 'asked_priority' : times_asking})

@app.route('/save_data', methods=['POST'])  # Example route definition
def save_data():
    # print("Incoming data:", request.json)
    # Retrieve data from the request
    user = request.json.get('sender')
    username = request.json.get('name')
    image = request.json.get('picture')
    chat_log = request.json.get('log')
    sentence1 = f"The {username} chat log history has been deleted"
    if chat_log == sentence1:

        return jsonify({"message": "Chat data is deleted."})

    else:
        # file_path = f"savechathistory/{username}.json"
        directory = 'chat_log_history'
        file_path = os.path.join(directory, f"{username}.json")
        # sentence1 = f"The {username} chat log history has been deleted"
        
        # print(f"Saving to: {file_path}")
        
        # Prepare the chat data
        chat_data = {
            "user": user,
            "image": image,
            "chatlog": chat_log
        }
        
        empty = {
            "user": None,
            "image": None,
            "chatlog": None
        }
        
        datas = {}
        os.makedirs("chat_log_history", exist_ok=True)

        # Try reading existing data, or create a new file if it doesn't exist
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    datas = json.load(f)
                    # print(datas[username])
                    print("accessed file")
            
            except json.JSONDecodeError:
                print("Error decoding JSON, starting with an empty dictionary.")
                datas = {}


                # datas = {}
        elif not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump({}, f)
                print("file not exist it was created")
                        
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump({}, f)
                print("file created")
            
        # Initialize the user's data if not present
        if username not in datas:
            datas[username] = []

        # Check if the chat_data is empty
        if empty == chat_data:
            return jsonify({"message": "Chat data is empty, not saved."}), 400
        
        # Append the new chat data to the existing data
        datas[username].append(chat_data)

        # Write the updated data back to the JSON file
        with open(file_path, "w") as f:
            json.dump(datas, f, indent=4)

        # Return a valid response
        return jsonify({"message": "Chat data saved successfully."}), 200

@app.route('/get_data', methods = ["POST"])
# def get_data():
#     username = request.json.get('name')
    
#     filename = f"chat_log_history/{username}.json"
    
#     if not os.path.isfile(filename):
#         return jsonify({"recent_chat_log": "File not found"})
    
#     else:
#         with open(f"chat_log_history/{username}.json", 'r') as f:
#             data = json.load(f)
    
#     Data_return = data[username]
#     return jsonify({"recent_chat_log" : Data_return}), 200
def get_data():
    username = request.json.get('name')
    filename = f"chat_log_history/{username}.json"

    if not os.path.isfile(filename):
        return jsonify({"recent_chat_log": "File not found"}), 404

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        Data_return = data.get(username, [])
        return jsonify({"recent_chat_log": Data_return}), 200
    except json.JSONDecodeError:
        return jsonify({"recent_chat_log": "Error loading chat log, file may be corrupted."}), 500

@app.route('/username_history', methods = ['POST'])
def username_history ():

    username = request.json.get('name')
    file_path = f"chat_log_history/{username}.json"

    # Check if the file exists
    if os.path.exists(file_path):
        exists = True
    else:
        exists = False
            
        print(exists)
    return jsonify({"Bool": exists})

@app.route('/is_valid_username', methods = ['POST'])
def vaild_username():
    def is_valid_username(username):
        # Username must contain only alphabetic characters (and optionally spaces)
        return bool(re.match("^[A-Za-z ]+$", username))
    username = request.json.get('name')
    vaild_name = is_valid_username(username)
    return jsonify({'valid' : vaild_name})
            
if __name__ == '__main__':
    app.run(debug=True)
    
# let use play game when ask question about pakpaokite more than 3 time
# add loading animation for the chatbot from the start 
