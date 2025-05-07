# 🔹 app/agents/query_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

def generate_inferred_paper(topic: str, references: list[str]) -> str:
    joined_refs = "\n".join(references)
    prompt = ChatPromptTemplate.from_template("""
너는 과학 논문 작성 도우미야.

주제: {topic}
참고 논문:
{references}

다음 형식을 따라 논문을 작성해줘:
[서론] [문제정의] [연구목적] [실험방법] [결과예상] [결론]
""")
    chain = prompt | llm
    return chain.invoke({"topic": topic, "references": joined_refs}).content
