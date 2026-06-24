STEP #1: Starting out 

Main link: https://ollama.com/  

Documentation: https://docs.ollama.com/  

Download: https://ollama.com/download  

 

Download Ubuntu Linux Server: 
https://ubuntu.com/download/server  

 

Install Linux onto computer. 

 
After install: 
• sudo apt update && sudo apt upgrade –y 

Make sure Curl is installed 

• sudo apt install curl –y 

Install Ollama 

• curl -fsSL https://ollama.com/install.sh | sh 

Install Specific model. Check here for models: ( https://ollama.com/search ) 

• sudo pull (model_name) 

Find a model you want. Here we want to use qwen3.6 ( https://ollama.com/library/qwen3.6 ) 

Aftering pulling a model you'll be able to interact with it. Use Ctrl + D to exit and when you want to interact with the mode again run: 

•sudo run (model_name) 

 

STEP #2: API Configuration 

Once Ollama is on the system, the api service should come over as well. To interact with the model through api do the following: 
• run: sudo systemctl status ollama  to see if the ollama is running 
•after that run: sudo systemctl edit ollama  this will let you edit the service file. 
•Drop this in the service file: 
[Service] 

Environment="OLLAMA_HOST=0.0.0.0:11434" 

•save and edit and run: sudo systemctl restart ollama. You can also run: sudo systemctl status ollama after to see if the service is running connectly. 
 
In your browser type the following: 
curl http://IP_ADDRESS:11434/api/tags 

•grab the ip address of what computer has the ai model on it. 
Once this loads you should see the model. 
 
Test: 
open up powershell and run this: 
$body = @{ 

  model = "qwen3.5:latest" 

  prompt = "Write a short joke about computers" 

} | ConvertTo-Json 

  

Invoke-RestMethod http://IP_ADDRESS/api/generate -Method Post -Body $body 
 
It will take a few minutes but you should see the model reply to you in powershell. 
