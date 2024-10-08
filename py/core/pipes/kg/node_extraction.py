# pipe to extract nodes/triples etc

import asyncio
import logging
import random
from typing import Any, AsyncGenerator, Optional
from uuid import UUID

from core.base import (
    AsyncState,
    CompletionProvider,
    EmbeddingProvider,
    KGProvider,
    PipeType,
    PromptProvider,
    RunLoggingSingleton,
)
from core.base.pipes.base_pipe import AsyncPipe

logger = logging.getLogger(__name__)


class KGNodeExtractionPipe(AsyncPipe):
    """
    The pipe takes input a list of documents (optional) and extracts nodes and triples from them.
    """

    class Input(AsyncPipe.Input):
        message: Any

    def __init__(
        self,
        kg_provider: KGProvider,
        llm_provider: CompletionProvider,
        prompt_provider: PromptProvider,
        config: AsyncPipe.PipeConfig,
        pipe_logger: Optional[RunLoggingSingleton] = None,
        type: PipeType = PipeType.OTHER,
        *args,
        **kwargs,
    ):
        super().__init__(
            pipe_logger=pipe_logger,
            type=type,
            config=config,
        )
        self.kg_provider = kg_provider
        self.llm_provider = llm_provider
        self.prompt_provider = prompt_provider

    async def _run_logic(  # type: ignore
        self,
        input: Input,
        state: AsyncState,
        run_id: UUID,
        *args,
        **kwargs,
    ) -> AsyncGenerator[Any, None]:

        nodes = self.kg_provider.get_entity_map()  # type: ignore

        for _, node_info in nodes.items():
            for entity in node_info["entities"]:
                yield entity, node_info[
                    "triples"
                ]  # the entity and its associated triples


class KGNodeDescriptionPipe(AsyncPipe):
    """
    The pipe takes input a list of nodes and extracts description from them.
    """

    class Input(AsyncPipe.Input):
        message: dict[str, Any]

    def __init__(
        self,
        kg_provider: KGProvider,
        llm_provider: CompletionProvider,
        embedding_provider: EmbeddingProvider,
        config: AsyncPipe.PipeConfig,
        pipe_logger: Optional[RunLoggingSingleton] = None,
        type: PipeType = PipeType.OTHER,
        *args,
        **kwargs,
    ):
        super().__init__(
            pipe_logger=pipe_logger,
            type=type,
            config=config,
        )
        self.kg_provider = kg_provider
        self.llm_provider = llm_provider
        self.embedding_provider = embedding_provider

    async def _run_logic(  # type: ignore
        self,
        input: AsyncPipe.Input,
        state: AsyncState,
        run_id: UUID,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncGenerator[Any, None]:
        """
        Extracts description from the input.
        """

        summarization_content = """
            Provide a comprehensive yet concise summary of the given entity, incorporating its description and associated triples:

            Entity: {entity_info}
            Description: {description}
            Triples: {triples_txt}

            Your summary should:
            1. Clearly define the entity's core concept or purpose
            2. Highlight key relationships or attributes from the triples
            3. Integrate any relevant information from the existing description
            4. Maintain a neutral, factual tone
            5. Be approximately 2-3 sentences long

            Ensure the summary is coherent, informative, and captures the essence of the entity within the context of the provided information.
        """

        async def process_entity(
            entity, triples, max_description_input_length
        ):

            # if embedding is present in the entity, just return it
            # in the future disable this to override and recompute the descriptions for all entities
            if entity.description_embedding:
                return entity

            entity_info = f"{entity.name}, {entity.description}"
            triples_txt = [
                f"{i+1}: {triple.subject}, {triple.object}, {triple.predicate} - Summary: {triple.description}"
                for i, triple in enumerate(triples)
            ]

            # truncate the descriptions to the max_description_input_length
            # randomly shuffle the triples
            # randomly select elements from the triples_txt until the length is less than max_description_input_length
            random.shuffle(triples_txt)
            truncated_triples_txt = ""
            current_length = 0
            for triple in triples_txt:
                if current_length + len(triple) > max_description_input_length:
                    break
                truncated_triples_txt += triple + "\n"
                current_length += len(triple)

            messages = [
                {
                    "role": "user",
                    "content": summarization_content.format(
                        entity_info=entity_info,
                        description=entity.description,
                        triples_txt=triples_txt,
                    ),
                }
            ]

            out_entity = self.kg_provider.retrieve_cache(
                "entities_with_description", f"{entity.name}_{entity.category}"
            )
            if out_entity:
                logger.info(f"Hit cache for entity {entity.name}")
            else:
                completion = await self.llm_provider.aget_completion(
                    messages,
                    self.kg_provider.config.kg_enrichment_settings.generation_config,
                )
                entity.description = completion.choices[0].message.content

                # embedding
                description_embedding = (
                    await self.embedding_provider.async_get_embeddings(
                        [entity.description]
                    )
                )
                entity.description_embedding = description_embedding[0]

                # name embedding
                # turned it off because we aren't using it for now
                # name_embedding = (
                #     await self.embedding_provider.async_get_embeddings(
                #         [entity.name]
                #     )
                # )
                # entity.name_embedding = name_embedding[0]

                out_entity = entity

            return out_entity

        max_description_input_length = input.message[
            "max_description_input_length"
        ]
        node_extractions = input.message["node_extractions"]

        tasks = []
        count = 0
        async for entity, triples in node_extractions:
            tasks.append(
                asyncio.create_task(
                    process_entity(
                        entity, triples, max_description_input_length
                    )
                )
            )
            count += 1

        logger.info(f"KG Node Description pipe: Created {count} tasks")
        # do gather because we need to wait for all descriptions before kicking off the next step
        processed_entities = await asyncio.gather(*tasks)

        # upsert to the database
        self.kg_provider.upsert_entities(
            processed_entities, with_embeddings=True
        )

        logger.info(
            "KG Node Description pipe: Upserted entities to the database"
        )

        for entity in processed_entities:
            yield entity
