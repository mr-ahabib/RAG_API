from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatHistory
from .rag_utils import retrieve_top_k_chunks, generate_groq_answer

@api_view(['POST'])
def chat_view(request):
    user_id = request.data.get("user_id", "anonymous")
    query = request.data.get("query")

    if not query:
        return Response({"error": "Query is required"}, status=400)

    top_chunks = retrieve_top_k_chunks(query)
    answer = generate_groq_answer(query, top_chunks)

    ChatHistory.objects.create(user_id=user_id, question=query, answer=answer)

    # Return last 10 chats of the user for chat history
    history_qs = ChatHistory.objects.filter(user_id=user_id).order_by('-timestamp')[:10]
    history = [{"question": c.question, "answer": c.answer} for c in history_qs]

    return Response({
        "answer": answer,
        "top_chunks": top_chunks,
        "history": history
    })
