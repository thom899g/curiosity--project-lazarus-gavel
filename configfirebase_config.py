"""
Firebase Admin SDK configuration for Project Lazarus Gavel.
Uses service account credentials from environment variable.
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.exceptions import FirebaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class FirebaseManager:
    """Singleton manager for Firebase connections with error recovery."""
    
    _instance = None
    _db = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance
    
    def initialize(self) -> bool:
        """Initialize Firebase Admin SDK with error handling."""
        if self._initialized:
            return True
            
        try:
            # Get service account credentials from environment
            cred_json = os.getenv('FIREBASE_SERVICE_ACCOUNT')
            if not cred_json:
                logger.error("FIREBASE_SERVICE_ACCOUNT environment variable not set")
                return False
                
            # Parse JSON credentials
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            
            # Initialize with error handling for duplicate apps
            try:
                firebase_admin.initialize_app(cred)
            except ValueError as e:
                if "already exists" in str(e):
                    # App already initialized, get existing app
                    logger.info("Firebase app already initialized")
                else:
                    raise
            
            self._db = firestore.client()
            self._initialized = True
            logger.info("Firebase initialized successfully")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in FIREBASE_SERVICE_ACCOUNT: {e}")
            return False
        except FirebaseError as e:
            logger.error(f"Firebase initialization error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected initialization error: {e}")
            return False
    
    @property
    def db(self) -> firestore.Client:
        """Get Firestore client with lazy initialization."""
        if not self._initialized:
            if not self.initialize():
                raise RuntimeError("Firebase failed to initialize")
        return self._db
    
    def close(self):
        """Clean up Firebase resources."""
        if self._initialized:
            firebase_admin.delete_app(firebase_admin.get_app())
            self._initialized = False
            self._db = None
            logger.info("Firebase connection closed")

# Global instance
firebase_manager = FirebaseManager()