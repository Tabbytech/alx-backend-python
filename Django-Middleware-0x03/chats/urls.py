
from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, ConversationListView, MessageListCreateView, MessageViewSet

# ✅ Now matches "routers.DefaultRouter()"
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# ✅ Now uses "NestedDefaultRouter"
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
    path('messages/', MessageListCreateView.as_view(), name='message_list_create'),
    path('conversations/', ConversationListView.as_view(), name='conversation_list'),
]
