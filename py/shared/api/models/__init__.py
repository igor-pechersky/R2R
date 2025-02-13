from shared.api.models.auth.responses import (
    TokenResponse,
    WrappedTokenResponse,
)
from shared.api.models.base import (
    GenericBooleanResponse,
    GenericMessageResponse,
    PaginatedR2RResult,
    R2RResults,
    WrappedBooleanResponse,
    WrappedGenericMessageResponse,
)
from shared.api.models.graph.responses import (
    GraphResponse,
    WrappedCommunitiesResponse,
    WrappedCommunityResponse,
    WrappedEntitiesResponse,
    WrappedEntityResponse,
    WrappedGraphResponse,
    WrappedGraphsResponse,
    WrappedRelationshipResponse,
    WrappedRelationshipsResponse,
)
from shared.api.models.ingestion.responses import (
    IngestionResponse,
    WrappedIngestionResponse,
    WrappedMetadataUpdateResponse,
    WrappedUpdateResponse,
    WrappedVectorIndexResponse,
    WrappedVectorIndicesResponse,
)
from shared.api.models.management.responses import (
    AnalyticsResponse,
    ChunkResponse,
    CollectionResponse,
    ConversationResponse,
    LogResponse,
    PromptResponse,
    ServerStats,
    SettingsResponse,
    WrappedAnalyticsResponse,
    WrappedAPIKeyResponse,
    WrappedAPIKeysResponse,
    WrappedChunkResponse,
    WrappedChunksResponse,
    WrappedCollectionResponse,
    WrappedCollectionsResponse,
    WrappedConversationMessagesResponse,
    WrappedConversationResponse,
    WrappedConversationsResponse,
    WrappedDocumentResponse,
    WrappedDocumentsResponse,
    WrappedLimitsResponse,
    WrappedLoginResponse,
    WrappedLogsResponse,
    WrappedMessageResponse,
    WrappedPromptResponse,
    WrappedPromptsResponse,
    WrappedServerStatsResponse,
    WrappedSettingsResponse,
    WrappedUserResponse,
    WrappedUsersResponse,
)
from shared.api.models.retrieval.responses import (
    AgentResponse,
    AggregateSearchResult,
    Citation,
    CitationData,
    CitationEvent,
    FinalAnswerData,
    FinalAnswerEvent,
    MessageData,
    MessageDelta,
    MessageEvent,
    RAGResponse,
    SearchResultsData,
    SearchResultsEvent,
    SSEEventBase,
    ToolCallData,
    ToolCallEvent,
    ToolResultData,
    ToolResultEvent,
    UnknownEvent,
    WrappedAgentResponse,
    WrappedDocumentSearchResponse,
    WrappedRAGResponse,
    WrappedSearchResponse,
    WrappedVectorSearchResponse,
)

__all__ = [
    # Generic Responses
    "SSEEventBase",
    "SearchResultsData",
    "SearchResultsEvent",
    "MessageDelta",
    "MessageData",
    "MessageEvent",
    "CitationData",
    "CitationEvent",
    "FinalAnswerData",
    "FinalAnswerEvent",
    "ToolCallData",
    "ToolCallEvent",
    "ToolResultData",
    "ToolResultEvent",
    "UnknownEvent",
    # Auth Responses
    "GenericMessageResponse",
    "TokenResponse",
    "WrappedTokenResponse",
    "WrappedGenericMessageResponse",
    # Ingestion Responses
    "IngestionResponse",
    "WrappedIngestionResponse",
    "WrappedUpdateResponse",
    "WrappedVectorIndexResponse",
    "WrappedVectorIndicesResponse",
    "WrappedMetadataUpdateResponse",
    "GraphResponse",
    "WrappedGraphResponse",
    "WrappedGraphsResponse",
    "WrappedEntityResponse",
    "WrappedEntitiesResponse",
    "WrappedRelationshipResponse",
    "WrappedRelationshipsResponse",
    "WrappedCommunityResponse",
    "WrappedCommunitiesResponse",
    # Management Responses
    "PromptResponse",
    "ServerStats",
    "LogResponse",
    "AnalyticsResponse",
    "SettingsResponse",
    "ChunkResponse",
    "CollectionResponse",
    "ConversationResponse",
    "WrappedServerStatsResponse",
    "WrappedLogsResponse",
    "WrappedAnalyticsResponse",
    "WrappedSettingsResponse",
    # Document Responses
    "WrappedDocumentResponse",
    "WrappedDocumentsResponse",
    # Collection Responses
    "WrappedCollectionResponse",
    "WrappedCollectionsResponse",
    # Prompt Responses
    "WrappedPromptResponse",
    "WrappedPromptsResponse",
    # Chunk Responses
    "WrappedChunkResponse",
    "WrappedChunksResponse",
    # Conversation Responses
    "WrappedConversationMessagesResponse",
    "WrappedConversationResponse",
    "WrappedConversationsResponse",
    # User Responses
    "WrappedUserResponse",
    "WrappedAPIKeyResponse",
    "WrappedLimitsResponse",
    "WrappedAPIKeysResponse",
    "WrappedLoginResponse",
    "WrappedUsersResponse",
    "WrappedMessageResponse",
    # Base Responses
    "PaginatedR2RResult",
    "R2RResults",
    "GenericBooleanResponse",
    "GenericMessageResponse",
    "WrappedBooleanResponse",
    "WrappedGenericMessageResponse",
    # TODO: Clean up the following responses
    # Retrieval Responses
    "RAGResponse",
    "Citation",
    "WrappedRAGResponse",
    "AgentResponse",
    "AggregateSearchResult",
    "WrappedSearchResponse",
    "WrappedDocumentSearchResponse",
    "WrappedVectorSearchResponse",
    "WrappedAgentResponse",
]
