from supabase import create_client, Client

# URL y clave pública de Supabase
url = "https://xgjyebgtttuybbaeppdo.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhnanllYmd0dHR1eWJiYWVwcGRvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkyNzQ0MTgsImV4cCI6MjA2NDg1MDQxOH0.tTg1OMuldC259v1QvlFrTwbjHl0ykPNNHgsK8V6CXyw"

# Crear el cliente de Supabase
supabase: Client = create_client(url, key)
