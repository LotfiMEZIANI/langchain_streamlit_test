from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.agents import load_tools, initialize_agent, AgentType


load_dotenv()


def generate_pet_name(
    animal_type: str, pet_color: str, suggestions_number: int
) -> dict[str, str]:
    llm = OpenAI(temperature=0.7)

    prompt_template_pet_name = PromptTemplate(
        input_variables=["animal_type", "pet_color", "suggestions_number"],
        template="I have a {animal_type} pet and I want a cool name for it. it has a {pet_color} color. Suggest me "
        + "{suggestions_number} cool names for my pet.",
    )

    name_chain = LLMChain(
        llm=llm, prompt=prompt_template_pet_name, output_key="pet_name"
    )

    response = name_chain(
        {
            "animal_type": animal_type,
            "pet_color": pet_color,
            "suggestions_number": suggestions_number,
        }
    )

    return response


def langchain_agent():
    llm = OpenAI(temperature=0.5)

    tools = load_tools(["wikipedia", "llm-math"], llm=llm)

    agent = initialize_agent(
        tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    response = agent.run("What is the average age of a dog? Multiple the age by 3")

    return response


if __name__ == "__main__":
    result = langchain_agent()

    print(result)
