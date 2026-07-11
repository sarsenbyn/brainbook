import PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
from fastapi.concurrency import run_in_threadpool
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from config.database.database import AsyncSession
from src.ai import get_embedding, generate_answer
from sqlalchemy import text

def text_extraction(element):
    line_text = element.get_text()
    
    line_formats = []

    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)

    format_per_line = set(line_formats)
    return (line_text, format_per_line)

def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    return table

def table_converter(table):
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    table_string = table_string[:-1]
    return table_string

def process_pdf_content(file_path):
    all_data = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_data.append({
                    "type": "table", 
                    "content": table_converter(table), 
                    "page": page.page_number
                })
            
            text = page.extract_text()
            if text and text.strip():
                all_data.append({
                    "type": "text", 
                    "content": text.strip(), 
                    "page": page.page_number
                })
                
    return all_data

def split_text_into_chunks(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100,
        length_function = len,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

async def semantic_search(query: str, db: AsyncSession):
    query_vector = await get_embedding(query)
    sql = text("""
        SELECT text, page_number 
        FROM documents 
        ORDER BY embedding <-> :query_vector 
        LIMIT 3
    """)
    result = await db.execute(sql, {"query_vector": str(query_vector)})
    return result.mappings().all()

async def ask_question(question: str, db: AsyncSession):
    search_results = await semantic_search(question, db)
    context_text = ""
    for result in search_results:
        text=result['text']
        page=result['page_number']

        fragment = f"Источник (страница {page}): {text}\n\n"
        context_text+=fragment
    prompt = f"""
    Ты — эксперт-помощник по учебнику. 
    Используй информацию ниже, чтобы ответить на вопрос пользователя.
    Если в текстах нет ответа, честно скажи, что не знаешь.
    Не придумывай факты, которых нет в источниках.
    Говори в каких страницах ты нашел ответ.

    Источники:
    {context_text}

    Вопрос пользователя: {question}
    """

    answer = await generate_answer(prompt)
    return answer