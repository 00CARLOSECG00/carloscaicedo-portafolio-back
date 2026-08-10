"""Static fallback content when Supabase is unavailable."""

from app.data.knowledge import KNOWLEDGE_NODES, static_knowledge_graph
from app.models.schemas import (
    Achievement,
    Certificate,
    Education,
    Experience,
    Language,
    MethodologyStep,
    Profile,
    ProfileContextChunk,
    ProfileLinks,
    Project,
)

FALLBACK_PROFILE = Profile(
    name="Carlos Caicedo",
    title="AI · Data · Machine Learning",
    tagline="I build intelligent systems where AI, data and technology intersect.",
    description="Interactive portfolio of Carlos Caicedo, exploring AI, data, machine learning and intelligent systems.",
    bio="Carlos Caicedo is an AI and data engineer focused on NLP, LLMs, RAG, and data architecture.",
    links=ProfileLinks(
        linkedin="https://www.linkedin.com/in/00carlos-caicedo00/",
        github="https://github.com/00CARLOSECG00",
        email="carloscaicedog2008@hotmail.com",
        resume="/resume.pdf",
    ),
    linkedin_handle="@00carlos-caicedo00",
    github_handle="@00CARLOSECG00",
)

FALLBACK_PROJECTS: list[Project] = [
    Project(
        id="talk-to-my-ai",
        title="Talk to My AI",
        description="A conversational assistant that knows my work. Ask about projects, experience or ideas and it answers with text and interactive cards.",
        category="AI Assistant",
        accent="primary",
        technologies=["LLMs", "RAG", "Streaming"],
        target="#ai",
    ),
    Project(
        id="nlp-playground",
        title="NLP Playground",
        description="Type any text and watch machines read it — sentiment, emotion, language, keywords and named entities, side by side.",
        category="Natural Language",
        accent="secondary",
        technologies=["NLP", "Classification"],
        target="#nlp",
    ),
    Project(
        id="database-lab",
        title="Database Lab",
        description="One dataset seen seven ways — relational, document, columnar, key-value, vector, graph and geospatial.",
        category="Data Architecture",
        accent="primary",
        technologies=["Data Modeling", "Vector Search"],
        target="#databases",
    ),
]

FALLBACK_EXPERIENCE: list[Experience] = [
    Experience(
        id="exp-freelance",
        company="Freelance / Personal Projects",
        role="AI & Data Engineer",
        description="Design and build intelligent systems — conversational AI, NLP pipelines, and multi-paradigm data architectures.",
        start_date="2024",
        end_date=None,
        is_current=True,
        technologies=["Python", "FastAPI", "Groq", "Supabase", "Next.js"],
    ),
]

FALLBACK_EDUCATION: list[Education] = [
    Education(
        id="edu-javeriana",
        institution="Pontificia Universidad Javeriana",
        degree="Systems Engineering",
        field="Computer Science & Engineering",
        description="Software engineering, data structures, machine learning fundamentals, and database systems.",
        start_date="2020",
        end_date="2025",
    ),
]

FALLBACK_METHODOLOGY: list[MethodologyStep] = [
    MethodologyStep(label="Problem", detail="Start from the real question, not the tools. What decision does this need to support?", sort_order=1),
    MethodologyStep(label="Understand the Data", detail="Explore shape, quality and meaning before assuming anything about it.", sort_order=2),
    MethodologyStep(label="Choose the Representation", detail="Relational, document, vector, graph or geospatial — pick the model that fits the question.", sort_order=3),
    MethodologyStep(label="Build", detail="Ship something interactive and measurable, not a slide deck.", sort_order=4),
    MethodologyStep(label="Evaluate", detail="Judge honestly against the original problem, with the right metrics.", sort_order=5),
    MethodologyStep(label="Improve", detail="Iterate on what the evaluation reveals — the loop is the product.", sort_order=6),
]

FALLBACK_LANGUAGES: list[Language] = [
    Language(id="lang-es", name="Spanish", proficiency="Native", sort_order=1),
    Language(id="lang-en", name="English", proficiency="Professional working proficiency", sort_order=2),
]

FALLBACK_CERTIFICATES: list[Certificate] = []

FALLBACK_ACHIEVEMENTS: list[Achievement] = [
    Achievement(
        id="ach-portfolio",
        title="Built an interactive AI portfolio",
        description="Connected a conversational assistant, NLP playground, and knowledge graph through a full-stack architecture.",
        sort_order=1,
    ),
]

FALLBACK_AI_SUGGESTIONS: list[str] = [
    "What does Carlos specialize in?",
    "Tell me about his AI projects.",
    "What is his work experience?",
    "What databases does he work with?",
    "How does he approach data problems?",
    "Tell me about RAG.",
]

FALLBACK_PROFILE_CONTEXT: list[ProfileContextChunk] = [
    ProfileContextChunk(
        category="bio",
        title="Professional summary",
        content="Carlos Caicedo specializes in AI, data and machine learning — NLP, LLMs, RAG, and data architecture.",
    ),
]
