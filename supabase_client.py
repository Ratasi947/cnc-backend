from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("https://czcxtrpgunuksiqvouhi.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN6Y3h0cnBndW51a3NpcXZvdWhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTgxMTAsImV4cCI6MjA5MDE5NDExMH0.QwpHKwsdW7ZpDhkHsI3BVgxYnTeg4Tm_8zPl-GE3uCo")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
