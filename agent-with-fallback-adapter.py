from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io, llm, stt, tts, inference
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel


load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.""",
        )

server = AgentServer()

@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
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
    )

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