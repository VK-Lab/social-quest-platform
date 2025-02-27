import os
from supabase import create_client
from typing import Optional
import logging

# Initialize Supabase client
try:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials")

    logging.info(f"Initializing Supabase client with URL: {supabase_url.split('://')[0]}://***")

    supabase = create_client(
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
    logging.info("Supabase client initialized successfully")
except Exception as e:
    logging.error(f"Error initializing Supabase client: {str(e)}")
    raise

def get_user_by_wallet(wallet_address: str) -> Optional[dict]:
    """Get user data from Supabase by wallet address"""
    try:
        logging.debug(f"Fetching user with wallet address: {wallet_address}")
        response = supabase.table('users').select("*").eq('wallet_address', wallet_address).execute()

        if hasattr(response, 'error') and response.error:
            logging.error(f"Supabase error fetching user: {response.error}")
            return None

        if response.data:
            logging.info(f"Found user with wallet address: {wallet_address}")
            return response.data[0]

        logging.info(f"No user found with wallet address: {wallet_address}")
        return None
    except Exception as e:
        logging.error(f"Exception in get_user_by_wallet: {str(e)}")
        return None

def create_user(wallet_address: str) -> Optional[dict]:
    """Create a new user in Supabase"""
    try:
        logging.debug(f"Creating new user with wallet address: {wallet_address}")
        # Insert user data as a list of dictionaries
        insert_data = [{
            'wallet_address': wallet_address,
            'xp_total': 0
        }]
        logging.debug(f"Insert data: {insert_data}")

        # Verify table exists before insert
        try:
            test_response = supabase.table('users').select("*").limit(1).execute()
            logging.debug(f"Table verification response: {test_response}")
        except Exception as table_error:
            logging.error(f"Error verifying users table: {str(table_error)}")
            return None

        # Attempt to insert the new user
        response = supabase.table('users').insert(insert_data).select("*").execute()
        logging.debug(f"Full Supabase response: {response}")

        if hasattr(response, 'error') and response.error:
            logging.error(f"Supabase error while creating user: {response.error}")
            return None

        if not response.data:
            logging.error("No data returned from user creation")
            return None

        created_user = response.data[0]
        logging.info(f"Created new user with ID: {created_user.get('id')} and wallet: {wallet_address}")
        return created_user

    except Exception as e:
        logging.error(f"Exception in create_user: {str(e)}")
        return None

def update_user_xp(user_id: int, xp_total: int) -> bool:
    """Update user's XP in Supabase"""
    try:
        logging.debug(f"Updating XP for user {user_id} to {xp_total}")
        response = supabase.table('users').update({
            'xp_total': xp_total
        }).eq('id', user_id).execute()

        if hasattr(response, 'error') and response.error:
            logging.error(f"Error updating XP: {response.error}")
            return False

        logging.info(f"Successfully updated XP for user {user_id}")
        return True
    except Exception as e:
        logging.error(f"Exception in update_user_xp: {str(e)}")
        return False

def get_leaderboard():
    """Get all users ordered by XP for leaderboard"""
    try:
        logging.debug("Fetching leaderboard data")
        response = supabase.table('users').select("*").order('xp_total', desc=True).execute()

        if hasattr(response, 'error') and response.error:
            logging.error(f"Error fetching leaderboard: {response.error}")
            return []

        logging.info(f"Retrieved leaderboard with {len(response.data)} entries")
        return response.data
    except Exception as e:
        logging.error(f"Exception in get_leaderboard: {str(e)}")
        return []