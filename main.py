from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai # استيراد مكتبة openai

# --- Configuration ---
# يفضل تحميل مفتاح الـ API من متغير بيئة لأسباب أمنية
# تأكد من تعيين هذا المتغير قبل تشغيل التطبيق (باستخدام set OPENAI_API_KEY=your_key_here في Windows)
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it before running the app.")

KNOWLEDGE_BASE_FILE = "knowledge_base.txt"

# --- FastAPI App ---
# لقد قمنا بتغيير العنوان ليعكس استخدام OpenAI
app = FastAPI(title="AI Q&A Assistant (Powered by OpenAI)", version="1.0")

# --- Pydantic Models ---
class UserMessage(BaseModel):
    message: str

class AIResponse(BaseModel):
    response: str

# --- Helper Function to Load Knowledge Base ---
def load_knowledge_base() -> str:
    """Reads and returns the content of the knowledge base file."""
    try:
        with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # إذا لم يتم العثور على الملف، يمكننا إرجاع رسالة افتراضية
        return "No knowledge base file found. Please create 'knowledge_base.txt' with your data."

# --- API Endpoint ---
@app.post("/ask", response_model=AIResponse)
async def ask_ai(user_message: UserMessage):
    """
    Accepts a user's message and returns an AI-generated response based on a knowledge base.
    """
    knowledge_base = load_knowledge_base()

    # إنشاء الموجه (prompt) لنموذج OpenAI
    # نستخدم دور "system" لتوجيه سلوك النموذج، ودور "user" لسؤال المستخدم وقاعدة المعرفة
    messages = [
        {"role": "system", "content": "أنت مساعد مفيد وذكي. أجب على أسئلة المستخدم بإيجاز ودقة، مستخدمًا فقط المعلومات المقدمة في 'قاعدة المعرفة'. إذا لم تكن الإجابة موجودة بوضوح في قاعدة المعرفة، فاذكر ببساطة 'عذرًا، لا أستطيع العثور على هذه المعلومات في قاعدة المعرفة المتاحة لي.'"},
        {"role": "user", "content": f"قاعدة المعرفة:\n{knowledge_base}\n\nسؤال المستخدم: {user_message.message}\n\nالإجابة:"}
    ]

    try:
        # استدعاء OpenAI API لإنشاء الاستجابة
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo", # نموذج قوي وفعال من حيث التكلفة لدعم اللغة العربية
            messages=messages,
            max_tokens=200, # التحكم في أقصى طول للإجابة للحفاظ على الإيجاز
            temperature=0.7 # التحكم في إبداع الاستجابة (0.0 للإجابات الأكثر تحديدًا، 1.0 للأكثر إبداعًا)
        )

        ai_response = completion.choices[0].message.content.strip()
        return AIResponse(response=ai_response)
    except openai.AuthenticationError:
        raise HTTPException(status_code=401, detail="OpenAI API key is invalid or missing. Please check your OPENAI_API_KEY environment variable.")
    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI API rate limit exceeded. Please wait or check your plan.")
    except Exception as e:
        # معالجة أي أخطاء أخرى قد تحدث أثناء استدعاء الـ API
        raise HTTPException(status_code=500, detail=f"An error occurred while communicating with OpenAI: {e}")