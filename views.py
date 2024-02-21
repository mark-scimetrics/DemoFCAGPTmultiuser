import os

from flask import Blueprint, jsonify, render_template, request, session
from openai import OpenAI


my_secret = os.environ['OpenAIKey']

bp = Blueprint('views', __name__, template_folder='templates')

countwer = 0
client = OpenAI(api_key=my_secret)
#assistant = client.beta.assistants.create(
#    name="FCA Chatbot",
#    description=
#    "FCA Regulatory Compliance Advisor will converse in UK #English. It will only respond on UK financial regulation. For #every piece of guidance given, FCA Regulatory Compliance Advisor #will cite the specific clause numbers from the official FCA #Handbook, and it will exclusively use the FCA Handbook as its #source for information, abstaining from referencing any other #materials.",
#    model="gpt-4-turbo-preview")

assistant = client.beta.assistants.retrieve("asst_EJiTpXaXUEMuHO98I2VvNAC6")




@bp.route('/')
def index():

  if 'visits' in session:
    session['visits'] = session.get('visits') + 1
    thread = client.beta.threads.create()
    session['thread_id']=thread.id
  else:
    session['visits'] = 0
    thread = client.beta.threads.create()
    session['thread_id']=thread.id
  
  print(f"Rendering INDEX {session.get('visits',-1)}")
  return render_template('index.html')


@bp.route('/submit', methods=['POST'])
def submit():
  global countwer
  #global thread
  #global run

  thread_id=session.get('thread_id')
  
  input_string = request.form['input_string']
  print(f"Visit number {session.get('visits',-1)}")

  if countwer == 0:
    client.beta.threads.messages.create(thread_id,
                                        role="user",                                       content=input_string)
    
    run = client.beta.threads.runs.create(thread_id=thread_id,
                            assistant_id=assistant.id)
    session['run_id']=run.id
  else:
    #Delete previous run and reset
    client.beta.threads.delete(thread_id)
    #Recreate new thread, message, run
    thread = client.beta.threads.create()
    session['thread_id']=thread.id
    thread_id=thread.id
    client.beta.threads.messages.create(thread_id,
                                        role="user",
                                  content=input_string)
    
    run = client.beta.threads.runs.create(thread_id=thread_id,
                              assistant_id=assistant.id)
    session['run_id']=run.id
    countwer = 0

  countwer = countwer + 1

  # Extract the message content

  return jsonify(message=input_string)


@bp.route('/poll')
def poll():
  # This function could be any Python function you wish to call periodically.
  global countwer
#  global thread
#  global run

  thread_id=session.get('thread_id')
  run_id=session.get('run_id')
  
  print(f"Visit number {session.get('visits',-1)}")
  if countwer > 0:
    run2 = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run_id)
    
    current_time = run2.status
    if current_time == "completed":
      # Retrieve the message object
      thread_messages = client.beta.threads.messages.list(thread_id)
      last_message = thread_messages.data[0].content[0]
      #   print(last_message.text.value)
      #  print(dir(last_message.text))
      # Extract the message content
      message_content = last_message.text.value
      return jsonify({'current_time': f"Visit number {session.get('visits',5)}" + message_content})
    else:
      return jsonify({'current_time': current_time})
  else:
    return jsonify({'current_time': "Not Ready"})
