import langchain_helper as lch
import streamlit as st


def main():
    st.set_page_config(page_title="Pet Name Generator", page_icon="🤖")

    pets_list = ["Cat", "Dog", "Fish", "Rabbit", "Hamster"]
    pet_color = None

    st.title("Pet Name Generator")

    suggestions_number = st.sidebar.number_input(
        label="How many suggestions do you want?",
        min_value=1,
        max_value=10,
        placeholder=5,
        value=5,
    )

    animal_type = st.sidebar.selectbox(label="what is your pet?", options=pets_list)

    if animal_type in pets_list:
        pet_color = st.sidebar.text_area(
            label=f"what is your {animal_type.lower()}'s color?", max_chars=15
        )

    if animal_type and pet_color and suggestions_number:
        response = lch.generate_pet_name(
            animal_type=animal_type,
            pet_color=pet_color,
            suggestions_number=suggestions_number,
        )

        st.text(response["pet_name"])


if __name__ == "__main__":
    main()
