from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3")


def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)

def parse_content(content):
    """
    Adobe Stock থেকে নিম্নলিখিত তথ্যগুলি পার্স করে:
    - ইমেজ ক্যাটাগরি
    - ভিডিও ডেটা
    - টেমপ্লেট ইনফরমেশন
    """
    parsed_data = {
        'categories': [],
        'media_items': [],
        'templates': []
    }
    
    try:
        # ক্যাটাগরি পার্স করা
        categories = content.find_all('div', {'class': 'category'})
        parsed_data['categories'] = [cat.text.strip() for cat in categories]
        
        # মিডিয়া আইটেম (ইমেজ/ভিডিও) পার্স করা
        media_items = content.find_all('div', {'class': 'media-item'})
        for item in media_items:
            media_info = {
                'type': item.get('data-type', ''),
                'duration': item.get('data-duration', ''),
                'quality': item.get('data-quality', ''),
                'url': item.get('data-url', '')
            }
            parsed_data['media_items'].append(media_info)
            
        # টেমপ্লেট ইনফরমেশন পার্স করা
        templates = content.find_all('div', {'class': 'template'})
        parsed_data['templates'] = [temp.text.strip() for temp in templates]
        
    except Exception as e:
        print(f"পার্সিং এরর: {str(e)}")
    
    return parsed_data
