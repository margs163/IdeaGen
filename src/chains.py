import os
from langchain_groq import ChatGroq
import langchain
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

groqapi_key = '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'
os.environ['GROQ_API_KEY'] = groqapi_key

groq_llm = ChatGroq(
    temperature = 0.5,
    model='llama3-70b-8192'
)


prompt_template_ideas = PromptTemplate(
        input_variables = ['input'],
        template = 'You are a project idea generator. Suggest science investigatory project name in the field and subject that human input - {input} contains, without any explanation.'
                    'Each time you are called, you generate completely new project idea. You do not need to explain anything.' 
                    'You have to give one creative idea that has to be completely different from the previous ideas you generated in the past: {history}. You output a string without quotation marks containing only the idea.'
)

memory = ConversationBufferWindowMemory()

idea_conv_chain = ConversationChain(llm = groq_llm, memory = memory, prompt = prompt_template_ideas, output_key = 'project_idea')

    # problem chain
prompt_template_problems = PromptTemplate(
        input_variables = ['project_idea'],
        template = 'Identify problems that the project {project_idea} adresses. You do not need to explain the problems that this project adresses.'
                    'Just give the problems, do not explain anything, just give problems associated with that project. You output a list containing only the problems.'
)
    
problem_chain = LLMChain(llm = groq_llm, prompt = prompt_template_problems, output_key='project_problem')


    # researching object chain
prompt_template_object = PromptTemplate(
        input_variables = ['project_idea, project_problem'],
        template = 'Identify objects that are being researched in the project {project_idea}. Do not explain anything, just generate'
        ' objects that can be researched in that project. You output a list containing only the objects.'
)
    
object_chain = LLMChain(llm = groq_llm, prompt = prompt_template_object, output_key='project_object')

    
    # sequential chain
project_chain = SequentialChain(
        chains = [idea_conv_chain, problem_chain, object_chain],
        input_variables = ['input'],
        output_variables = ['project_idea', 'project_problem', 'project_object']
)


def generate_project(subject: str, field: str) -> dict:

    #calling the sequential chain
    generated_text = project_chain.invoke(f'subject: {subject}, field: {field}')

    #returning the dict
    return {
        'project_ideas': generated_text['project_idea'],
        'project_problems': generated_text['project_problem'],
        'project_objects':  generated_text['project_object']
    }
 

# Chatbot

prompt_template_chatbot = PromptTemplate(
    input_variables=['user_input', 'project_idea'],
    template="You are a chatbot assistant that answers the users' questions, related to their projects. Users can generate their project ideas by clicking on filling the textboxes with information and clicking on 'Generate' button. You were created by Daniyal, and you help users in Daniyal's web applications. Be polite and creative when you give answers to users." 
    "Your main goal is to help users with their projects. The user's project idea: {project_idea}. \nAnswer the user's question: {user_input}"
)

chatbot_memory = ConversationBufferWindowMemory(k = 3, input_key='user_input')

chatbot = LLMChain(llm=groq_llm, prompt = prompt_template_chatbot, memory=chatbot_memory)

def generate_chatbot_response(input: str, idea: str):
    bot_text = chatbot.invoke({
        'user_input': input,
        'project_idea': idea
    })
    return bot_text


