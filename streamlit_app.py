import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 마켓 리뷰 분석")
st.write(
    "아래에 문서를 업로드하고 질문을 해보세요 – GPT가 답변해 드립니다!"
    "이 앱을 사용하려면 OpenAI API 키를 제공해야 합니다. API 키는 [여기](https://platform.openai.com/account/api-keys)에서 받을 수 있습니다. "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API 키를 입력해주세요.", type="password")
if not openai_api_key:
    st.info("API 키를 입력하시면 서비스를 이용할 수 있습니다.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "파일 업로드해주세요 (.xlsx, .csv, .txt 형식만 가능)", type=("xslx", "csv", "txt")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "문서에 대해 질문을 입력하세요!",
        placeholder="간단한 요약을 제공해 줄 수 있나요?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
