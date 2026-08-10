-- =============================================================================
-- Seed data — Carlos Caicedo Portfolio
-- Run AFTER schema.sql in Supabase SQL Editor
--
-- HOW TO UPDATE YOUR DATA:
--   • Profile:     UPDATE site_profile SET title = '...' WHERE id = 'default';
--   • Projects:    INSERT new rows or SET is_active = false on old ones
--   • Experience:  Same pattern — hide with is_active = false
--   • Education:   Same
--   • AI context:  Add rows to profile_context for Groq to read
--   • Knowledge:   INSERT/UPDATE knowledge_nodes
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Site profile
-- ---------------------------------------------------------------------------
INSERT INTO site_profile (
  id, name, title, tagline, description, bio,
  linkedin_url, github_url, email, resume_url,
  linkedin_handle, github_handle
) VALUES (
  'default',
  'Carlos Caicedo',
  'AI · Data · Machine Learning',
  'I build intelligent systems where AI, data and technology intersect.',
  'Interactive portfolio of Carlos Caicedo, exploring AI, data, machine learning and intelligent systems.',
  'Carlos Caicedo is an AI and data engineer focused on NLP, LLMs, RAG, and data architecture. He builds interactive systems that turn complex technical work into explorable experiences.',
  'https://www.linkedin.com/in/00carlos-caicedo00/',
  'https://github.com/00CARLOSECG00',
  'carloscaicedog2008@hotmail.com',
  '/resume.pdf',
  '@00carlos-caicedo00',
  '@00CARLOSECG00'
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  title = EXCLUDED.title,
  tagline = EXCLUDED.tagline,
  description = EXCLUDED.description,
  bio = EXCLUDED.bio,
  linkedin_url = EXCLUDED.linkedin_url,
  github_url = EXCLUDED.github_url,
  email = EXCLUDED.email,
  resume_url = EXCLUDED.resume_url,
  linkedin_handle = EXCLUDED.linkedin_handle,
  github_handle = EXCLUDED.github_handle,
  updated_at = NOW();

-- ---------------------------------------------------------------------------
-- Projects — reorder with sort_order; hide old ones with is_active = false
-- ---------------------------------------------------------------------------
INSERT INTO projects (id, title, description, category, accent, technologies, target, sort_order, is_active) VALUES
  (
    'talk-to-my-ai',
    'Talk to My AI',
    'A conversational assistant that knows my work. Ask about projects, experience or ideas and it answers with text and interactive cards.',
    'AI Assistant',
    'primary',
    ARRAY['LLMs', 'RAG', 'Groq', 'Streaming'],
    '#ai',
    1,
    true
  ),
  (
    'nlp-playground',
    'NLP Playground',
    'Type any text and watch machines read it — sentiment, emotion, language, keywords, entities and summarization, side by side.',
    'Natural Language',
    'secondary',
    ARRAY['NLP', 'TextBlob', 'YAKE'],
    '#nlp',
    2,
    true
  ),
  (
    'database-lab',
    'Database Lab',
    'One dataset seen seven ways — relational, document, columnar, key-value, vector, graph and geospatial. Representation is a design choice.',
    'Data Architecture',
    'primary',
    ARRAY['PostgreSQL', 'Vector Search', 'Graph'],
    '#databases',
    3,
    true
  )
ON CONFLICT (id) DO UPDATE SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  category = EXCLUDED.category,
  accent = EXCLUDED.accent,
  technologies = EXCLUDED.technologies,
  target = EXCLUDED.target,
  sort_order = EXCLUDED.sort_order,
  is_active = EXCLUDED.is_active,
  updated_at = NOW();

-- Example: hide an old project without deleting it
-- UPDATE projects SET is_active = false WHERE id = 'old-project-slug';

-- ---------------------------------------------------------------------------
-- Work experience — add your real roles here
-- ---------------------------------------------------------------------------
INSERT INTO experience (company, role, description, start_date, end_date, is_current, technologies, sort_order) VALUES
  (
    'Freelance / Personal Projects',
    'AI & Data Engineer',
    'Design and build intelligent systems — conversational AI assistants, NLP pipelines, and multi-paradigm data architectures. This portfolio is a live demonstration of that work.',
    '2024',
    NULL,
    true,
    ARRAY['Python', 'FastAPI', 'Groq', 'Supabase', 'Next.js'],
    1
  ),
  (
    'University Projects',
    'Machine Learning Developer',
    'Developed ML and NLP projects applying classification, sentiment analysis, and data visualization across structured and unstructured datasets.',
    '2022',
    '2024',
    false,
    ARRAY['Python', 'scikit-learn', 'Pandas', 'NLP'],
    2
  );

-- ---------------------------------------------------------------------------
-- Education
-- ---------------------------------------------------------------------------
INSERT INTO education (institution, degree, field, description, start_date, end_date, sort_order) VALUES
  (
    'Pontificia Universidad Javeriana',
    'Systems Engineering',
    'Computer Science & Engineering',
    'Focused on software engineering, data structures, machine learning fundamentals, and database systems.',
    '2020',
    '2025',
    1
  );

-- ---------------------------------------------------------------------------
-- Languages, certificates and achievements
-- ---------------------------------------------------------------------------
TRUNCATE languages, certificates, achievements RESTART IDENTITY;
INSERT INTO languages (name, proficiency, sort_order) VALUES
  ('Spanish', 'Native', 1),
  ('English', 'Professional working proficiency', 2);

INSERT INTO certificates (title, issuer, issue_date, sort_order) VALUES
  ('Certificate title', 'Issuer name', 'YYYY', 1);

INSERT INTO achievements (title, description, sort_order) VALUES
  ('Built an interactive AI portfolio', 'Connected LLMs, NLP and data architecture into a full-stack experience that can be explored live.', 1);

-- ---------------------------------------------------------------------------
-- Methodology ("How I Think")
-- ---------------------------------------------------------------------------
TRUNCATE methodology_steps RESTART IDENTITY;
INSERT INTO methodology_steps (label, detail, sort_order) VALUES
  ('Problem', 'Start from the real question, not the tools. What decision does this need to support?', 1),
  ('Understand the Data', 'Explore shape, quality and meaning before assuming anything about it.', 2),
  ('Choose the Representation', 'Relational, document, vector, graph or geospatial — pick the model that fits the question.', 3),
  ('Build', 'Ship something interactive and measurable, not a slide deck.', 4),
  ('Evaluate', 'Judge honestly against the original problem, with the right metrics.', 5),
  ('Improve', 'Iterate on what the evaluation reveals — the loop is the product.', 6);

-- ---------------------------------------------------------------------------
-- AI chat suggestions
-- ---------------------------------------------------------------------------
TRUNCATE ai_suggestions RESTART IDENTITY;
INSERT INTO ai_suggestions (text, sort_order) VALUES
  ('What does Carlos specialize in?', 1),
  ('Tell me about his AI projects.', 2),
  ('What is his work experience?', 3),
  ('What databases does he work with?', 4),
  ('How does he approach data problems?', 5),
  ('Tell me about RAG.', 6);

-- ---------------------------------------------------------------------------
-- Profile context — free text Groq reads to answer questions about you
-- Add, edit or deactivate rows (is_active = false) anytime
-- ---------------------------------------------------------------------------
INSERT INTO profile_context (category, title, content, sort_order) VALUES
  (
    'bio',
    'Professional summary',
    'Carlos Caicedo specializes in AI, data and machine learning. He builds intelligent systems at the intersection of NLP, LLMs, RAG, embeddings, vector databases, and multi-paradigm data architecture.',
    1
  ),
  (
    'skills',
    'Core technical skills',
    'Python, FastAPI, Next.js, TypeScript, PostgreSQL/Supabase, Groq LLMs, NLP (sentiment, NER, summarization), RAG patterns, data modeling across relational/document/vector/graph/geospatial paradigms.',
    2
  ),
  (
    'highlight',
    'Portfolio as a product',
    'This portfolio itself is a technical demonstration: a conversational AI assistant, NLP playground, database lab showing seven data paradigms, and an interactive knowledge graph — all connected through a backend-agnostic REST API.',
    3
  ),
  (
    'general',
    'Approach to problems',
    'Carlos follows a deliberate loop: understand the problem, explore the data, choose the right representation, build, evaluate, and improve. He treats database choice and data modeling as design decisions, not defaults.',
    4
  );

-- ---------------------------------------------------------------------------
-- Knowledge graph nodes
-- ---------------------------------------------------------------------------
INSERT INTO knowledge_nodes (id, label, group_name, description, related, projects, technologies, sort_order) VALUES
  ('ai', 'Artificial Intelligence', 'core', 'Systems that reason, learn and act on data to solve problems that once needed a human.', ARRAY['ml','nlp','llms','ai-apps'], ARRAY['talk-to-my-ai'], NULL, 1),
  ('ml', 'Machine Learning', 'ai', 'Learning patterns from data instead of hand-writing rules — the engine behind most modern AI.', ARRAY['ai','embeddings','vector-db'], NULL, ARRAY['scikit-learn','PyTorch'], 2),
  ('nlp', 'NLP', 'ai', 'Teaching machines to read, understand and generate human language.', ARRAY['ai','llms','embeddings'], ARRAY['nlp-playground'], NULL, 3),
  ('llms', 'LLMs', 'ai', 'Large language models that generate and reason over text, powering assistants and RAG.', ARRAY['nlp','rag','ai'], ARRAY['talk-to-my-ai'], NULL, 4),
  ('rag', 'RAG', 'ai', 'Retrieval-Augmented Generation connects language models with external knowledge sources so answers stay grounded and current.', ARRAY['embeddings','vector-db','llms'], ARRAY['talk-to-my-ai'], NULL, 5),
  ('embeddings', 'Embeddings', 'data', 'Numeric representations of meaning that let machines compare text, images and records by similarity.', ARRAY['rag','vector-db','nlp'], NULL, NULL, 6),
  ('retrieval', 'Retrieval', 'data', 'Finding the most relevant pieces of knowledge for a query before generation happens.', ARRAY['rag','vector-db'], NULL, NULL, 7),
  ('ai-apps', 'AI Applications', 'ai', 'Turning models into real products — assistants, search, analytics and automation.', ARRAY['ai','llms'], ARRAY['talk-to-my-ai','nlp-playground'], NULL, 8),
  ('databases', 'Databases', 'core', 'The many ways data can be stored and queried — each shaped by the questions you need to answer.', ARRAY['relational','document','columnar','key-value','vector-db','graph','geospatial'], ARRAY['database-lab'], NULL, 9),
  ('relational', 'Relational', 'db', 'Tables, rows and joins — the reliable default for structured, related data.', ARRAY['databases'], NULL, NULL, 10),
  ('document', 'Document', 'db', 'Flexible JSON-like documents that keep related data together.', ARRAY['databases'], NULL, NULL, 11),
  ('columnar', 'Columnar', 'db', 'Column-oriented storage built for fast analytics over huge datasets.', ARRAY['databases'], NULL, NULL, 12),
  ('key-value', 'Key-Value', 'db', 'Blazing-fast lookups by key — ideal for caching and sessions.', ARRAY['databases'], NULL, NULL, 13),
  ('vector-db', 'Vector Databases', 'db', 'Store embeddings and search by meaning rather than exact matches — the backbone of RAG.', ARRAY['databases','embeddings','rag'], ARRAY['database-lab'], NULL, 14),
  ('graph', 'Graph', 'db', 'Nodes and relationships that make connected data a first-class citizen.', ARRAY['databases'], NULL, NULL, 15),
  ('geospatial', 'Geospatial', 'db', 'Data anchored to places, queried by distance, region and shape.', ARRAY['databases'], NULL, NULL, 16)
ON CONFLICT (id) DO UPDATE SET
  label = EXCLUDED.label,
  group_name = EXCLUDED.group_name,
  description = EXCLUDED.description,
  related = EXCLUDED.related,
  projects = EXCLUDED.projects,
  technologies = EXCLUDED.technologies,
  sort_order = EXCLUDED.sort_order;

INSERT INTO knowledge_edges (source, target) VALUES
  ('ai', 'ml'), ('ai', 'nlp'), ('ai', 'llms'), ('ai', 'ai-apps'),
  ('ml', 'embeddings'), ('ml', 'vector-db'),
  ('nlp', 'llms'), ('nlp', 'embeddings'),
  ('llms', 'rag'),
  ('rag', 'embeddings'), ('rag', 'vector-db'),
  ('databases', 'relational'), ('databases', 'document'), ('databases', 'columnar'),
  ('databases', 'key-value'), ('databases', 'vector-db'), ('databases', 'graph'), ('databases', 'geospatial')
ON CONFLICT DO NOTHING;
