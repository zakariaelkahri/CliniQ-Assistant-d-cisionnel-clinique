from app.rag.retriever import retriever
from app.rag.llm import gamini_model, local_model 
from app.rag.prompt import structured_prompt_template

def answer_question(user_question: str) -> str:
    docs = retriever.invoke(user_question)
    
    context = " ".join([doc.page_content for doc in docs])
    
    formatted_prompt = structured_prompt_template.format(
        context=context,
        question=user_question
    )
    
    llm = local_model()
    response = llm.invoke(formatted_prompt)
    return response.content

    # llm = gamini_model()
    # response = llm.generate_content(formatted_prompt) 
    # return response.text

# answer = answer_question("Dans l’asthme, quand le salbutamol doit-il être répété toutes les 20 minutes ?")
# print(answer)
