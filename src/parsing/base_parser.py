"""
Base parser class for GTO chart data extraction.
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List, Union, Any


class BaseGTOParser(ABC):
    """
    Abstract base class for GTO chart parsers.
    
    This class defines the interface that all chart parsers should implement.
    Each subclass will handle a specific format (PDF, HTML, etc.)
    """
    
    @abstractmethod
    def parse(self, file_path: str) -> pd.DataFrame:
        """
        Parse a GTO chart file into a standardized DataFrame.
        
        Args:
            file_path: Path to the chart file to parse
            
        Returns:
            DataFrame with standardized columns:
                - context: Poker context (e.g., "BTN_RFI_25bb", "SB_VS_BB_CALL_10bb")
                - hand_range: Hand or range (e.g., "AA", "KQs", "JTs-87s")
                - action: Action to take (e.g., "raise", "call", "fold")
                - frequency: Frequency of action (0-100)
                - eff_stack: Effective stack in big blinds
        """
        pass
    
    @abstractmethod
    def _identify_format(self, file_path: str) -> bool:
        """
        Check if the file can be parsed by this parser.
        
        Args:
            file_path: Path to the chart file to check
            
        Returns:
            True if the file can be parsed, False otherwise
        """
        pass
    
    @abstractmethod
    def _extract_metadata(self, content: Any) -> Dict[str, Any]:
        """
        Extract metadata from the chart file content.
        
        Args:
            content: The content of the chart file
            
        Returns:
            Dictionary containing metadata (e.g., stack sizes, positions)
        """
        pass
    
    def standardize_hand_notation(self, hand: str) -> str:
        """
        Convert hand notation to a standard format.
        
        Args:
            hand: Hand in original notation
            
        Returns:
            Hand in standardized notation (e.g., "AKs", "TT", "98o")
        """
        # Convert main hand to uppercase but keep suited/offsuit indicator case
        hand = hand.strip()
        
        # Special case for pairs
        if len(hand) == 2 and hand[0].upper() == hand[1].upper():
            return hand.upper()
        
        # Handle suited/offsuit notation
        if len(hand) == 2:
            # Assume suited if not specified
            return hand.upper() + "s"
        elif len(hand) == 3:
            # Maintain case of the last character (s/o indicator)
            rank_chars = hand[:2].upper()
            suit_indicator = hand[2].lower()  # Convention is lowercase 's' or 'o'
            return rank_chars + suit_indicator
            
        # For ranges or more complex notation, keep as is but uppercase ranks
        return hand 