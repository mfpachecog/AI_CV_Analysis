try:
    from langchain_community.chat_models import ChatOpenAI
    print("Imported ChatOpenAI from community")
except ImportError:
    print("ChatOpenAI not found in community")
