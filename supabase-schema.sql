-- ═══════════════════════════════════════════════════════════
-- ROSANNA & ANDREW WEDDING — Supabase Database Schema
-- Project: devaibz | https://hyalpsznjfuhpamzruyg.supabase.co
-- Run this in your Supabase SQL Editor
-- ═══════════════════════════════════════════════════════════

-- 1. RSVPS TABLE
-- Stores all guest RSVP responses (submitted through rsvp.html)
-- and manually added guests (through admin.html)

CREATE TABLE IF NOT EXISTS public.rsvps (
  id                    UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  
  -- Guest Identity
  first_name            TEXT NOT NULL,
  last_name             TEXT NOT NULL,
  email                 TEXT,
  phone                 TEXT,          -- WhatsApp number with country code e.g. +15017250604
  
  -- RSVP Status
  attendance            TEXT CHECK (attendance IN ('attending', 'maybe', 'declined', 'invited')),
  
  -- Plus One
  plus_one              BOOLEAN DEFAULT FALSE,
  plus_one_name         TEXT,
  
  -- Meal & Dietary
  meal_preference       TEXT,          -- chicken / fish / vegetarian / vegan
  dietary_requirements  TEXT,          -- comma-separated
  
  -- Fun Extras
  song_request          TEXT,
  message               TEXT,          -- note/message for couple
  
  -- Tracking
  opened_at             TIMESTAMPTZ,   -- when they first opened the invite (future: track via pixel/link)
  created_at            TIMESTAMPTZ DEFAULT NOW(),
  updated_at            TIMESTAMPTZ DEFAULT NOW()
);

-- 2. ROW LEVEL SECURITY (RLS)
-- Allow anyone to INSERT (submit RSVP), but only service role can SELECT/UPDATE/DELETE
-- This is managed in the admin panel with your anon key for now (adjust for production)

ALTER TABLE public.rsvps ENABLE ROW LEVEL SECURITY;

-- Allow INSERT for anonymous users (guests submitting RSVP)
CREATE POLICY "Allow public insert" ON public.rsvps
  FOR INSERT TO anon
  WITH CHECK (true);

-- Allow SELECT for anonymous users (for admin panel — tighten in production)
-- In production: replace anon with authenticated role and add admin auth
CREATE POLICY "Allow public read" ON public.rsvps
  FOR SELECT TO anon
  USING (true);

-- Allow UPDATE for anon (admin edits)
CREATE POLICY "Allow public update" ON public.rsvps
  FOR UPDATE TO anon
  USING (true);

-- Allow DELETE for anon (admin removes)
CREATE POLICY "Allow public delete" ON public.rsvps
  FOR DELETE TO anon
  USING (true);

-- 3. AUTO-UPDATE timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER rsvps_updated_at
  BEFORE UPDATE ON public.rsvps
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- 4. SAMPLE DATA — uncomment to test
/*
INSERT INTO public.rsvps (first_name, last_name, email, phone, attendance, plus_one) VALUES
  ('Maria', 'Garcia',   'maria@example.com',  '+15011234567', 'attending', true),
  ('John',  'Williams', 'john@example.com',   '+15019876543', 'attending', false),
  ('Sarah', 'Johnson',  'sarah@example.com',  '+15015551234', 'maybe',     false),
  ('Carlos','Reyes',    'carlos@example.com', '+15014445678', 'declined',  false),
  ('Emma',  'Brown',    'emma@example.com',   '+15013334444', 'invited',   false);
*/

-- ═══════════════════════════════════════════════════════════
-- USEFUL QUERIES FOR THE COUPLE
-- ═══════════════════════════════════════════════════════════

-- Count by attendance status:
-- SELECT attendance, COUNT(*) FROM rsvps GROUP BY attendance;

-- Total headcount (attending + their plus ones):
-- SELECT 
--   SUM(CASE WHEN attendance = 'attending' THEN 1 ELSE 0 END) as guests,
--   SUM(CASE WHEN attendance = 'attending' AND plus_one THEN 1 ELSE 0 END) as plus_ones,
--   SUM(CASE WHEN attendance = 'attending' THEN (CASE WHEN plus_one THEN 2 ELSE 1 END) ELSE 0 END) as total_headcount
-- FROM rsvps;

-- Guests with dietary requirements:
-- SELECT first_name, last_name, dietary_requirements FROM rsvps 
-- WHERE dietary_requirements IS NOT NULL AND dietary_requirements != '';

-- Song requests:
-- SELECT first_name, song_request FROM rsvps WHERE song_request IS NOT NULL;

-- Recent RSVPs:
-- SELECT first_name, last_name, attendance, created_at FROM rsvps 
-- ORDER BY created_at DESC LIMIT 20;
