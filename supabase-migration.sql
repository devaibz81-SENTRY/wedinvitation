-- ═══════════════════════════════════════════════════════════
-- ROSANNA & ANDREW WEDDING — Safe Migration
-- Skips anything that already exists
-- ═══════════════════════════════════════════════════════════

-- 1. Add any missing columns to existing rsvps table
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='phone') THEN
    ALTER TABLE public.rsvps ADD COLUMN phone TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='plus_one') THEN
    ALTER TABLE public.rsvps ADD COLUMN plus_one BOOLEAN DEFAULT FALSE;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='plus_one_name') THEN
    ALTER TABLE public.rsvps ADD COLUMN plus_one_name TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='meal_preference') THEN
    ALTER TABLE public.rsvps ADD COLUMN meal_preference TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='dietary_requirements') THEN
    ALTER TABLE public.rsvps ADD COLUMN dietary_requirements TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='song_request') THEN
    ALTER TABLE public.rsvps ADD COLUMN song_request TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='message') THEN
    ALTER TABLE public.rsvps ADD COLUMN message TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='opened_at') THEN
    ALTER TABLE public.rsvps ADD COLUMN opened_at TIMESTAMPTZ;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='attendance') THEN
    ALTER TABLE public.rsvps ADD COLUMN attendance TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='first_name') THEN
    ALTER TABLE public.rsvps ADD COLUMN first_name TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='last_name') THEN
    ALTER TABLE public.rsvps ADD COLUMN last_name TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='email') THEN
    ALTER TABLE public.rsvps ADD COLUMN email TEXT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='updated_at') THEN
    ALTER TABLE public.rsvps ADD COLUMN updated_at TIMESTAMPTZ DEFAULT NOW();
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='rsvps' AND column_name='created_at') THEN
    ALTER TABLE public.rsvps ADD COLUMN created_at TIMESTAMPTZ DEFAULT NOW();
  END IF;
END $$;

-- 2. Drop and recreate policies cleanly
DROP POLICY IF EXISTS "Allow public insert" ON public.rsvps;
DROP POLICY IF EXISTS "Allow public read"   ON public.rsvps;
DROP POLICY IF EXISTS "Allow public update" ON public.rsvps;
DROP POLICY IF EXISTS "Allow public delete" ON public.rsvps;

CREATE POLICY "Allow public insert" ON public.rsvps FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "Allow public read"   ON public.rsvps FOR SELECT TO anon USING (true);
CREATE POLICY "Allow public update" ON public.rsvps FOR UPDATE TO anon USING (true);
CREATE POLICY "Allow public delete" ON public.rsvps FOR DELETE TO anon USING (true);

-- 3. Auto-update trigger (safe)
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS rsvps_updated_at ON public.rsvps;
CREATE TRIGGER rsvps_updated_at
  BEFORE UPDATE ON public.rsvps
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- 4. Verify — should show all columns
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'rsvps'
ORDER BY ordinal_position;
