from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)
MEDICINES_FILE = r"C:\Users\Lenovo\OneDrive\Desktop\medivoice-ai\data\medicine_dataset_detailed.json"

# Load dataset
with open(MEDICINES_FILE, 'r', encoding='utf-8') as f:
    medicines = json.load(f)

# Helper to find medicine by partial match
def find_medicine(transcript):
    t = transcript.lower()
    for m in medicines:
        if t in m['name'].lower():
            return m
    tokens = t.split()
    for m in medicines:
        for token in tokens:
            if token in m['name'].lower():
                return m
    return None

# Helper to get requested field
def get_requested_field(transcript, med):
    q = transcript.lower()
    # Trigger phrases
    triggers = ['hey murfmedu', 'hey medu', 'hey murf medu']
    if any(t in q for t in triggers):
        return "yes tell me"
    # Medicine fields
    field = None
    if any(w in q for w in ['use','uses','ka use','kya karta','what is']):
        field = 'uses'
    elif any(w in q for w in ['prescription','prescribe','doctor']):
        field = 'prescription'
    elif any(w in q for w in ['dosage','dose','kitni','kitna']):
        field = 'dosage'
    if field and med.get(field):
        return f"{med['name']} - {med.get(field)}"
    return f"{med['name']} - Info not available for requested field"

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Medu</title>
<style>
body {margin:0;font-family:Arial,sans-serif;background:linear-gradient(135deg,#3b0a8a,#6c00ff);display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;color:#fff;text-align:center;}
h1{font-size:3em;margin:0.2em 0;}
.button{display:flex;flex-direction:column;align-items:center;justify-content:center;width:120px;height:120px;border-radius:50%;background-color:#5f3eff;cursor:pointer;transition:all 0.3s ease;margin:10px;}
.button:hover{transform:scale(1.1);}
#mic.active{background-color:#ff3f81;}
#speaker.green{background-color:#2ecc71;}
.input-box{display:flex;width:50%;max-width:500px;margin-top:20px;}
.input-box input{flex:1;padding:0.8em;border-radius:25px 0 0 25px;border:none;outline:none;font-size:1em;}
.input-box button{padding:0.8em 1.5em;border-radius:0 25px 25px 0;border:none;background-color:#ff3f81;color:#fff;cursor:pointer;font-size:1em;}
.input-box button:hover{background-color:#ff6090;}
</style>
</head>
<body>
<h1>AI MEDU</h1>
<div class="button" id="mic"><i class="fas fa-microphone" style="font-size:2.5em;"></i><span>Mic</span></div>
<div class="button" id="speaker"><i class="fas fa-volume-up" style="font-size:2.5em;"></i><span>AI Response</span></div>
<div class="input-box">
<input type="text" id="manualText" placeholder="Type your question here">
<button id="sendText">Send</button>
</div>
<script>
const mic=document.getElementById('mic');
const speaker=document.getElementById('speaker');
const sendText=document.getElementById('sendText');
const manualText=document.getElementById('manualText');

let voices=[];
function loadVoices(){
    voices=speechSynthesis.getVoices().filter(v=>v.lang.includes('en-IN')||v.name.includes('Indian'));
}
speechSynthesis.onvoiceschanged = loadVoices;

// Speak function
function speak(text){
    const utter=new SpeechSynthesisUtterance(text);
    utter.voice=voices[0]||null;
    utter.lang='en-IN';
    utter.onstart=()=>speaker.classList.add('green');
    utter.onend=()=>speaker.classList.remove('green');
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
}

// Process text (from mic or manual input)
async function processText(txt){
    if(!txt) return;
    try{
        const r=await fetch('/query',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({text:txt})
        });
        const j=await r.json();
        let reply=j.reply||'Medicine not found.';
        // Trigger response
        const triggers=['hey murfmedu','hey medu','hey murf medu'];
        if(triggers.some(t=>txt.toLowerCase().includes(t))){
            speak('yes tell me');
        } else {
            speak(reply);
        }
    }catch(e){ alert('Network error: '+e);}
}

// Manual text input
sendText.onclick=()=>{processText(manualText.value.trim());}

// Mic recognition (start/stop)
let recognition=null;
if('webkitSpeechRecognition' in window){
    recognition = new webkitSpeechRecognition();
    recognition.lang='en-IN';
    recognition.interimResults=false;
    recognition.continuous=false; // Auto-stop after speaking
    recognition.onstart=()=>mic.classList.add('active');
    recognition.onend=()=>mic.classList.remove('active');
    recognition.onresult=e=>{
        const transcript=e.results[0][0].transcript;
        processText(transcript);
    };
}

mic.onclick=()=>{ if(recognition) recognition.start(); }

</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
</body>
</html>
""")

@app.route('/query', methods=['POST'])
def query_text():
    data=request.get_json() or {}
    txt=data.get('text','').strip()
    if not txt: return jsonify(error='No text provided'), 400
    found=find_medicine(txt)
    if found:
        reply=get_requested_field(txt, found)
    else:
        reply="Medicine not found."
    return jsonify(reply=reply)

if __name__=='__main__':
    app.run(debug=True)


