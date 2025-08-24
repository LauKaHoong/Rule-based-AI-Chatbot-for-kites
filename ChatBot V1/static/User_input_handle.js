document.addEventListener('DOMContentLoaded', (event) => { // make sure that the html file is loaded before javascript
    
    let totalTimesPriority = 0;

    function Display_recent_chat (data){
        console.log('Data received for chat display: ',data)

        const chatBox = document.querySelector('#chat-box'); // Ensure chatBox is defined here
        const user = data.user;
        const image = data.image;
        const messageText = data.chatlog;

        console.log('User:', user, 'Image:', image, 'Message Text:', messageText);

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + (user === 'user' ? 'user-message' : 'bot-message');

        const profileImg = document.createElement('img');
        profileImg.className = 'Image';
        profileImg.src = user === 'user' ? 'static/image/UserProfile.png' : 'static/image/quiz.jpg';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';

        const currentTime = document.createElement('div');
        currentTime.className = 'timestamp';
        updateDateTime(currentTime);

        if (user === 'bot') {
            // If the bot has an image, display it
            if (image) {
                const botImage = document.createElement('img');
                botImage.className = 'image';
                botImage.src = image;
                textDiv.appendChild(currentTime);
                textDiv.appendChild(botImage);
                console.log("Accessed")

            }
        }
    
        if (messageText) {
            const userMessageText = document.createElement('span');
            userMessageText.textContent = messageText; 
            textDiv.appendChild(currentTime);
            textDiv.appendChild(userMessageText);
        } else {
            console.warn('No message text available to display.'); 
        }

        // if (user === 'bot' && image) {
        //     const botImage = document.createElement('img');
        //     botImage.className = 'image';
        //     botImage.src = image; // Set the image source if it exists
        //     textDiv.appendChild(currentTime);
        //     textDiv.appendChild(botImage);
        //      // Append bot image if it exists
        // }

        // if (messageText) { // Ensure messageText is defined
        //     const userMessageText = document.createElement('span');
        //     userMessageText.textContent = messageText; // Set the message text
        //     textDiv.appendChild(currentTime);
        //     textDiv.appendChild(userMessageText);
        // } else {
        //     console.warn('No message text available to display.'); // Warn if there's no message text
        // }

         // Assuming you have a function to handle date/time
        messageDiv.appendChild(profileImg);
        messageDiv.appendChild(textDiv);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    function check_chat_log_username(username) {
        return fetch('/username_history', { // Ensure the fetch call is returned
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: username })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // This returns a promise that resolves to JSON
        })
        .then(data => {
            return data.Bool; // This returns the boolean value
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            return false; // Handle the error gracefully by returning false
        });
    };

    function get_chat_log (username){

        fetch('/get_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify({ name: username })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const chatBox = document.querySelector('#chat-box');
            chatBox.innerHTML = "" // remove the element inside the chatbox in order to add recent chat log data
            console.log('Chat log retrieved:', data.recent_chat_log);
            // console.log(data.recent_chat_log[0])
            // console.log(data.recent_chat_log[0]['user'])
            data.recent_chat_log.forEach(entry => {
                
                Display_recent_chat(entry);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    };

    function saveChatLog (user, image, chatLog, username){
        console.log({
            sender: user,
            name: username,
            picture: image,
            log: chatLog
        });

        fetch('/save_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            
            body: JSON.stringify({
                sender: user, 
                picture: image, 
                log: chatLog, 
                name: username
            }),
        }).then(response => response.json())
          .then(data => {
            console.log('Chat log saved:', data.message);
          });
    };

    function updateDateTime(elements) { //update only time
        const now = new Date();
        const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: true };
        const currentTime = now.toLocaleTimeString([], timeOptions); // Get formatted time
        
        elements.textContent = ` ${currentTime}`; // Display time
    };

    function Greeting (username){
        const now = new Date();
        const Current_hour  = now.getHours();
        const sender = "bot";
        setTimeout(() => {
            let intent = '';
            if (Current_hour > 6 && Current_hour <= 12) {
                intent = `Good morning ${username}, how may I help you?`;
            } else if (Current_hour > 12 && Current_hour <= 18) {
                intent = `Good Afternoon ${username}, how may I help you?`;
            } else if (Current_hour > 18 && Current_hour <= 24) {
                intent = `Good evening ${username}, how may I help you?`;
            } else {
                intent = `${username} Go to sleep`;
            }
            DisplayMassage(sender, intent, null);
            saveChatLog(sender, null, intent, username);
        }, 3000);
    };

    const responses = { // for image
        "pakpaokite" : 
        {
            image:
            [ 
            "static/image/pakpaokite7.jpg",
            "static/image/Screenshot_2024-10-08_162614.png"
        ]
        }
    };

    function startRecognition() {
        // Check if SpeechRecognition is supported
        if (!('webkitSpeechRecognition' in window)) {
            alert('Speech Recognition API not supported in this browser.');
            return;
        }

        // Create a new SpeechRecognition instance
        const recognition = new webkitSpeechRecognition(); // Use `SpeechRecognition` for non-WebKit browsers

        recognition.lang = 'en-US'; // Set language
        recognition.interimResults = false; // Set to true if you want to get interim results
        recognition.maxAlternatives = 1; // Number of alternatives to return

        recognition.onstart = function() {
            console.log('Speech recognition started');
        };

        recognition.onresult = function(event) { // return the result of the speech processed to text
            const transcript = event.results[0][0].transcript;
            DisplayMassage('user', transcript);
            sendTextToBackend(transcript);
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error', event.error);
        };

        recognition.onend = function() {
            console.log('Speech recognition ended');
        };

        recognition.start();
    };

    function Word_Delay(response, delay, textDiv) { 
        response.split('').forEach((char, i) => setTimeout(() => textDiv.innerHTML += char, i * delay));
    };

    function Loading_dot (Textdiv, delay){
        const Dot = document.createElement('div')
        Dot.classList.add('loading-dot');

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement("span");

            Dot.appendChild(dot);
        }

        Textdiv.appendChild(Dot)

        setTimeout(() => {Dot.remove();}, delay)
    };

    function sendTextToBackend(transcript) {
        const Delayed = 1000
        fetch('/ChatBot', {  // Ensure this matches your Flask route
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ textarea: transcript })  // Send the transcript as JSON
        })
        .then(response => response.json())
        .then(data => {
            let splited = data.input.split(" ")
            for (let i of splited){
                if (i in responses){
                    let Responsess = responses[i];
        
                    // Randomly select an image from the array
                    const images = Responsess.image;
                    const randomIndex = Math.floor(Math.random() * images.length);
                    const selectedImage = images[randomIndex]; // Get a random image

                    console.log("Keyword:", i);
                    console.log("Selected Image:", selectedImage);

                    setTimeout(() => {DisplayMassage('bot', null, selectedImage)}, Delayed)
                }
            }
            setTimeout(() => {DisplayMassage('bot', data.output, null);}, Delayed * 2)

        })
        .catch(error => console.error('Error sending data to backend:', error));
    };

    function DisplayMassage (sender, messageText, image){
        const Loading_delay = 2000
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + (sender === 'user' ? 'user-message' : 'bot-message');

        const profileImg = document.createElement('img');
        profileImg.className = 'Image';
        profileImg.src = sender === 'user' ? 'static/image/UserProfile.png' : 'static/image/quiz.jpg'; // Add image paths for user and bot

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';

        const currentTime = document.createElement('div');
        currentTime.className = 'timestamp';
        
        updateDateTime(currentTime);
        
        if (sender != 'user'){
            Loading_dot(textDiv, Loading_delay)
            
            if(image){
                setTimeout(() =>{
                const BotImage = document.createElement("img");
                BotImage.className = 'image';
                BotImage.src = image; // Set the image source
                textDiv.innerHTML = "";
                textDiv.appendChild(currentTime);
                textDiv.appendChild(BotImage);
                }, Loading_delay)
            }

            if (messageText){
                const userInput = document.querySelector(".userInput");
                // userInput.setAttribute('readonly', true); // make the textarea readonly
                setTimeout(() =>{
                let total_delay = messageText.length * 50;
                textDiv.innerHTML = "";
                Word_Delay(messageText, 50, textDiv);
                textDiv.appendChild(currentTime);
                setTimeout(() => {userInput.removeAttribute('readonly');}, total_delay); // make the textarea become editable
                }, Loading_delay)
                
            }
            
        }

        else
        {
            const userMessageText = document.createElement('span');
            userMessageText.textContent = messageText; // Set the message text
            textDiv.appendChild(currentTime);
            textDiv.appendChild(userMessageText);
        }
        messageDiv.appendChild(profileImg);
        messageDiv.appendChild(textDiv);

        // Append the entire message div to the chat box
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

    };

    function sendInput() {
        times_priority(totalTimesPriority).then(result => {
        console.log(result)
        const userInput = document.querySelector('.userInput').value.trim();
        const Delayed = 1000
        const username = document.getElementById('username-input').value;
        
        if (userInput === "") return;

        DisplayMassage('user', userInput, null)
        saveChatLog("user", null, userInput, username) // save user input

        fetch('/ChatBot',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // inform the server that the body of request is JSON- formatted data
            },
            body: JSON.stringify({ textarea: userInput, name :username , priority: result})
        })
        .then(response => response.json())
        .then(data => {
             // save the bot output 
            console.log(data.input)
            let attempt = 0;
            let splited = data.input.split(" ");
            
            console.log('Before update:', totalTimesPriority);
            totalTimesPriority += data.asked_priority; // Example line
            console.log('After update:', totalTimesPriority);

            for (let i of splited){
                if (attempt >= 1){
                    break;
                }
                
                if (i in responses){
                    let Responsess = responses[i];
        
                    // Randomly select an image from the array
                    const images = Responsess.image;
                    const randomIndex = Math.floor(Math.random() * images.length);
                    const selectedImage = images[randomIndex]; // Get a random image
                    console.log(selectedImage)
                    setTimeout(() => {DisplayMassage("bot", null, selectedImage)}, Delayed)
                    saveChatLog("bot", selectedImage, null, username)
                    attempt += 1;
                }
                
            }

            setTimeout(() => {DisplayMassage("bot", data.output, null);}, Delayed * 2)
            if (data.output == "We will start the puzzle game now"){
                window.location.href = '/puzzle'
            }
            else if (data.output == "We will start the quiz game now"){
                window.location.href = '/quizz'
            }
            saveChatLog("bot", null, data.output, username)
        })
        .catch(error => {
            console.error('Fetch error:', error); // Log the error
            DisplayMassage('bot', 'Error: ' + error.message)
        });

        document.querySelector('.userInput').value = '';})
    };

    function handleUsername() {
        const username = document.getElementById('username-input').value;
        const errorMessage = document.getElementById('error-message');
        
        vaild_username(username) .then (valid =>
            {   
            if (valid)
                {
                saveChatLog(null, null, null, username)
                if (username) 
                    {
                    sessionStorage.setItem('name', username);
                    errorMessage.style.display = 'none';
                    document.getElementById('username-box').classList.add('hidden');
                    document.getElementById('welcome-message').classList.remove('hidden');
                    document.getElementById('welcome-text').textContent = 'Welcome, ' + username + '!';

                    setTimeout(() => {
                        const welcomeMessage = document.getElementById('welcome-message');
                        welcomeMessage.classList.add('visible');
                        setTimeout(() => {
                            welcomeMessage.classList.remove('visible');

                            setTimeout(() => {
                                welcomeMessage.classList.add('hidden');
                                document.querySelector('.PakPaoKiteBot').classList.remove('hidden');
                                document.querySelector('.PakPaoKiteBot').classList.add('visible');
                            }, 1000);
                        }, 2000);
                    }, 0);

                    check_chat_log_username(username).then(exist => {
                        if (exist) 
                        {
                            get_chat_log(username);
                        } 
                        else 
                        {
                            Greeting(username); // Call Greeting if the user does not exist
                        }
                    }
                );
                } 
                else 
                {
                    document.getElementById('welcome-text').textContent = 'Please enter your username.';
                }
                }
                else{
                    errorMessage.style.display = 'block';
                }
            }
        )
    };

    function vaild_username (username){
        return fetch ('/is_valid_username', {
            method: 'POST',
            headers: {
                'Content-type' : 'application/json'
            },
            body: JSON.stringify({ name: username})
        })
        .then(response => response.json())
        .then(data => {
            return data.valid 
        })
    };

    function times_priority (currentTotal){
        const userInput = document.querySelector('.userInput').value.trim();
        const username = document.getElementById('username-input').value;

        return fetch ('/ChatBot', {
            method: 'POST',
            headers: {
                'Content-type' : 'application/json'
            },
            body: JSON.stringify({ textarea: userInput, name :username })
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.asked_priority !== undefined) {
                currentTotal += data.asked_priority; // Update the total here
                console.log('Updated priority:', totalTimesPriority);
                return currentTotal; // Return the updated total
            } 
            else {
                console.error('Invalid response data:', data);
                return null;  // Return null if the data structure is not as expected
            }
        })
        .catch(error => {
            console.error('Error fetching priority:', error);
            return null;  // Return null or a fallback value in case of an error
        });
    }

    const sendButton = document.querySelector('#send-button');
    const chatBox = document.querySelector('#chat-box');
    const userInput = document.querySelector(".userInput");
    const closeButton = document.getElementById('close-button');
    const openChatbotButton = document.getElementById('open-chatbot');
    const chatbot = document.querySelector('.PakPaoKiteBot');

    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            userInput.setAttribute('readonly', true);
            sendInput();
        }
    });

    sendButton.addEventListener('click', () => {
        userInput.setAttribute('readonly', true);
        sendInput()
    });

    document.getElementById('Microphone').addEventListener('click', startRecognition);

    closeButton.addEventListener('click', function() {
        chatbot.classList.add('hidden');
        setTimeout(() => {
            openChatbotButton.classList.add('visible');
            openChatbotButton.classList.remove('hidden');
        }, 500);
    });

    openChatbotButton.addEventListener('click', function() {
        chatbot.classList.remove('hidden');
        openChatbotButton.classList.add('hidden');
        setTimeout(() => {
            openChatbotButton.classList.remove('visible');
        }, 500);
    });

    closeButton.addEventListener('click', function() {
        chatbot.classList.add('hidden');
        chatbot.classList.remove('visible');
        setTimeout(() => {
            openChatbotButton.classList.remove('hidden');
            openChatbotButton.classList.add('visible');
        }, 500);
    });

    openChatbotButton.addEventListener('click', function() {
        chatbot.classList.remove('hidden');
        chatbot.classList.add('visible');
        openChatbotButton.classList.add('hidden');
        setTimeout(() => {
            openChatbotButton.classList.remove('visible');
        }, 500);
    });
    
    // document.getElementById('Username-button').addEventListener('click', handleUsername);
    document.getElementById('Username-button').addEventListener('click', handleUsername);
    document.getElementById('username-input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            handleUsername();
        }
    });
    
    const returnToChat = sessionStorage.getItem('returnToChat');

    if (returnToChat === 'true') {
        console.log("Returning to chat...");
        // Show the chatbox and hide the username input
        document.querySelector('.PakPaoKiteBot').classList.remove('hidden');
        document.getElementById('username-box').classList.add('hidden');

        // Optionally load the previous chat log
        const savedName = sessionStorage.getItem('name'); // Get the saved name
        if (savedName) {
            get_chat_log(savedName); // Load chat history if available
        }

        // Clear the flag after using it
        sessionStorage.removeItem('returnToChat');}
});