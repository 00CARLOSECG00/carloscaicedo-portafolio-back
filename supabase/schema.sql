-- =============================================================================
-- Carlos Caicedo Portfolio — Supabase / PostgreSQL schema
-- Run in Supabase SQL Editor: https://supabase.com/dashboard → SQL → New query
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Site profile (single row — update this when your title or links change)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS site_profile (
  id TEXT PRIMARY KEY DEFAULT 'default',
  name TEXT NOT NULL,
  title TEXT NOT NULL,
  tagline TEXT NOT NULL,
  description TEXT NOT NULL,
  bio TEXT,
  linkedin_url TEXT,
  github_url TEXT,
  email TEXT,
  resume_url TEXT DEFAULT '/resume.pdf',
  linkedin_handle TEXT,
  github_handle TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Projects (set is_active = false to hide without deleting)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  category TEXT NOT NULL,
  accent TEXT DEFAULT 'primary',
  technologies TEXT[] DEFAULT '{}',
  target TEXT,
  url TEXT,
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Work experience
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS experience (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company TEXT NOT NULL,
  role TEXT NOT NULL,
  description TEXT NOT NULL,
  start_date TEXT,
  end_date TEXT,
  is_current BOOLEAN DEFAULT false,
  technologies TEXT[] DEFAULT '{}',
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Education
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS education (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  institution TEXT NOT NULL,
  degree TEXT NOT NULL,
  field TEXT,
  description TEXT,
  start_date TEXT,
  end_date TEXT,
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Languages, certificates and achievements for the CV highlights section
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS languages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  proficiency TEXT,
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS certificates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  issuer TEXT,
  issue_date TEXT,
  credential_url TEXT,
  logo_url TEXT,
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- "How I Think" methodology steps
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS methodology_steps (
  id SERIAL PRIMARY KEY,
  label TEXT NOT NULL,
  detail TEXT NOT NULL,
  sort_order INT NOT NULL,
  is_active BOOLEAN DEFAULT true
);

-- ---------------------------------------------------------------------------
-- AI chat suggested prompts
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ai_suggestions (
  id SERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  sort_order INT NOT NULL,
  is_active BOOLEAN DEFAULT true
);

-- ---------------------------------------------------------------------------
-- Free-form context chunks fed to Groq (bio, highlights, skills narrative…)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS profile_context (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category TEXT NOT NULL CHECK (category IN ('bio', 'skills', 'highlight', 'general')),
  title TEXT,
  content TEXT NOT NULL,
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Knowledge graph
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS knowledge_nodes (
  id TEXT PRIMARY KEY,
  label TEXT NOT NULL,
  group_name TEXT NOT NULL,
  description TEXT NOT NULL,
  related TEXT[] DEFAULT '{}',
  projects TEXT[] DEFAULT '{}',
  technologies TEXT[] DEFAULT '{}',
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS knowledge_edges (
  source TEXT NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  target TEXT NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  PRIMARY KEY (source, target)
);

-- ---------------------------------------------------------------------------
-- Optional: conversation history
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id TEXT,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversations_conversation_id ON conversations(conversation_id);
CREATE INDEX IF NOT EXISTS idx_projects_active_sort ON projects(is_active, sort_order);
CREATE INDEX IF NOT EXISTS idx_experience_active_sort ON experience(is_active, sort_order);
CREATE INDEX IF NOT EXISTS idx_education_active_sort ON education(is_active, sort_order);

-- ---------------------------------------------------------------------------
-- Row Level Security — public read for portfolio content
-- ---------------------------------------------------------------------------
ALTER TABLE site_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE experience ENABLE ROW LEVEL SECURITY;
ALTER TABLE education ENABLE ROW LEVEL SECURITY;
ALTER TABLE languages ENABLE ROW LEVEL SECURITY;
ALTER TABLE certificates ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE methodology_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE profile_context ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_edges ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read site_profile" ON site_profile FOR SELECT USING (true);
CREATE POLICY "Public read projects" ON projects FOR SELECT USING (true);
CREATE POLICY "Public read experience" ON experience FOR SELECT USING (true);
CREATE POLICY "Public read education" ON education FOR SELECT USING (true);
CREATE POLICY "Public read languages" ON languages FOR SELECT USING (true);
CREATE POLICY "Public read certificates" ON certificates FOR SELECT USING (true);
CREATE POLICY "Public read achievements" ON achievements FOR SELECT USING (true);
CREATE POLICY "Public read methodology_steps" ON methodology_steps FOR SELECT USING (true);
CREATE POLICY "Public read ai_suggestions" ON ai_suggestions FOR SELECT USING (true);
CREATE POLICY "Public read profile_context" ON profile_context FOR SELECT USING (true);
CREATE POLICY "Public read knowledge_nodes" ON knowledge_nodes FOR SELECT USING (true);
CREATE POLICY "Public read knowledge_edges" ON knowledge_edges FOR SELECT USING (true);

-- Future RAG with pgvector:
-- CREATE EXTENSION IF NOT EXISTS vector;
-- CREATE TABLE document_embeddings (
--   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--   source TEXT NOT NULL,
--   content TEXT NOT NULL,
--   embedding vector(384),
--   metadata JSONB DEFAULT '{}'
-- );
