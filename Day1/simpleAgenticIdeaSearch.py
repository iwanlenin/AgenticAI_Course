import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print(f"OpenAI API Key exists and begins with {openai_api_key[:8]}")
else:
    print("OpenAI API Key does not exist")

openai = OpenAI() #wrapper over the OpenAI API

# create a message in format of openAI: role and content
# role is set to user
def create_message(content):
    return [{"role": "user", "content": content}]

# get response from openAI for the message
def get_response(messages):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return response.choices[0].message.content

def get_answer(question):
    messages = create_message(question)
    return get_response(messages)

# pick a business area that might be worth exploring for Agentic AI opportunity
llm_request = 'Pick a business area that might be worth exploring for Agentic AI opportunity. Respond only with area' 
# present the business idea
business_idea = get_answer(llm_request)
print("\nBusiness Area:")
print(business_idea)
# present a biggest painpoint in the business area
llm_request = 'Present a biggest painpoint in ' + business_idea + ' - something challenging that might be ripe for an Agentic solution. Answer with a list of 3 painpoints'
pain_points = get_answer(llm_request)
print("\nPain Points:")
print(pain_points)
#get the solution for the painpoint
# solution
llm_request = 'Create a solution for '+pain_points+' which can be a good and profitable agentic solution'
solution = get_answer(llm_request)
print("\nSolution:")
print(solution)






