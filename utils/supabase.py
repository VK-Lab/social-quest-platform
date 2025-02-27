import os
from supabase import create_client
from typing import Optional

# Initialize Supabase client
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

def get_user_by_wallet(wallet_address: str) -> Optional[dict]:
    """Get user data from Supabase by wallet address"""
    try:
        response = supabase.table('users').select("*").eq('wallet_address', wallet_address).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def create_user(wallet_address: str) -> Optional[dict]:
    """Create a new user in Supabase"""
    try:
        response = supabase.table('users').insert({
            'wallet_address': wallet_address,
            'xp_total': 0
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def update_user_xp(user_id: int, xp_total: int) -> bool:
    """Update user's XP in Supabase"""
    try:
        supabase.table('users').update({
            'xp_total': xp_total
        }).eq('id', user_id).execute()
        return True
    except Exception as e:
        print(f"Error updating user XP: {e}")
        return False

def get_leaderboard():
    """Get all users ordered by XP for leaderboard"""
    try:
        response = supabase.table('users').select("*").order('xp_total', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []
