import logging
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import JobContext, AgentServer,AgentSession, Agent, room_io, llm, stt, tts, inference, AgentStateChangedEvent, metrics, MetricsCollectedEvent
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
import time

logger = logging.getLogger(__name__)

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.""",
        )

server = AgentServer()


@server.rtc_session(agent_name="my-agent")
async def entrypoint(ctx: JobContext):

    session = AgentSession(
        stt= stt.FallbackAdapter(
            [
                inference.STT.from_model_string("deepgram/nova-3:multi"),
                inference.STT.from_model_string("assemblyai/assemblyai-1:multi"),
            ]
        ),
        llm= llm.FallbackAdapter(
            [
                inference.LLM.from_model_string("openai/gpt-4.1-mini"),  # This model is intentionally invalid to demonstrate fallback
                inference.LLM.from_model_string("google/gemini-2.5-flash"),
            ]
        ),
        tts=tts.FallbackAdapter(
            [
                inference.TTS.from_model_string("cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"),
                inference.TTS.from_model_string("google/tts:multi"),
            ]
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
        preemptive_generation=True,  # Enable preemptive generation to reduce latency   
    )

    # Set up metrics collection after session creation so we have access to session ID in the metrics callbacks    
    usage_collector = metrics.UsageCollector()
    last_eou_metrics = None

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        nonlocal last_eou_metrics
        if ev.metrics.type == "eou_metrics":
            last_eou_metrics = ev.metrics

        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)  
    
    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage summary: {summary}")

    ctx.add_shutdown_callback(log_usage)

    @session.on("agent_state_changed")
    def _on_agent_state_changed(ev: AgentStateChangedEvent):
        logger.info(f"Agent state changed: {ev.new_state}")
        if ev.new_state == "speaking" and last_eou_metrics is not None:
            elapsed = time.time() - last_eou_metrics.timestamp
            logger.info(f"Time to first audio: {elapsed:.2f} seconds")


    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )



if __name__ == "__main__":
    agents.cli.run_app(server)